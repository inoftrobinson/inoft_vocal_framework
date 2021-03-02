#[cfg(feature = "python36")] extern crate cpython36 as cpython;
#[cfg(feature = "python37")] extern crate cpython37 as cpython;
#[cfg(feature = "python38")] extern crate cpython38 as cpython;
#[cfg(feature = "python39")] extern crate cpython39 as cpython;

#[path="append.rs"] mod append;
#[path="decoder.rs"] pub mod decoder;
#[path="resampler.rs"] pub mod resampler;
#[path="renderer.rs"] pub mod renderer;
#[path="exporter.rs"] pub mod exporter;
#[path="parser.rs"] pub mod parser;
#[path="models.rs"] pub mod models;
#[path="audio_clip.rs"] pub mod audio_clip;
#[path="loader.rs"] pub mod loader;
#[path="hasher.rs"] pub mod hasher;
#[path="tracer.rs"] pub mod tracer;
#[path="saver.rs"] pub mod saver;
#[path="tests/mod.rs"] pub mod tests;

use std::borrow::Borrow;
use crate::resampler::resample;
use std::fs::File;
use std::path::Path;
use std::io::Write;
use crate::tracer::TraceItem;
use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject};
use crate::models::{ResampleSaveFileFromUrlData, ReceivedParsedData, ResampleSaveFileFromLocalFileData, ReceivedTargetSpec};
use symphonia_core::codecs::CodecParameters;
use hound::WavSpec;


py_module_initializer!(audio_engine, |py, m| {
    m.add(py, "__doc__", "Render dynamic audio.")?;
    m.add(py, "resample_save_file_from_local_file", py_fn!(py, resample_save_file_from_local_file(data: PyObject)))?;
    m.add(py, "resample_save_file_from_url", py_fn!(py, resample_save_file_from_url(data: PyObject)))?;
    m.add(py, "render", py_fn!(py, render(data: PyObject)))?;
    Ok(())
});


async fn execute_resample_save_file_from_vec(trace: &mut TraceItem, samples: Vec<i16>, codec_params: CodecParameters, target_spec: &ReceivedTargetSpec) {
    let resamples = resample(trace, samples, codec_params, target_spec.to_wav_spec());
    saver::save_samples(trace, resamples, target_spec, String::from("desired_filename_example")).await;
}

async fn execute_resample_save_file_from_local_file(data: ResampleSaveFileFromLocalFileData) -> bool {
    let trace = &mut TraceItem::new(String::from("Resample save file from local filepath"));
    let (samples, codec_params) = decoder::decode_from_local_filepath(
        trace, &*data.source_filepath, 0.0, None
    );
    execute_resample_save_file_from_vec(trace, samples.unwrap(), codec_params.unwrap(), &data.target_spec).await;
    trace.close();
    true
}

async fn execute_resample_save_file_from_url(data: ResampleSaveFileFromUrlData) -> bool {
    let trace = &mut TraceItem::new(String::from("Resample save file from url"));
    let (samples, codec_params) = decoder::decode_from_file_url(
        trace, &*data.file_url, 0.0, None
    ).await;
    execute_resample_save_file_from_vec(trace, samples.unwrap(), codec_params.unwrap(), &data.target_spec).await;
    trace.close();
    true
}

pub fn resample_save_file_from_local_file(_py: Python, data: PyObject) -> PyResult<bool> {
    let parsed_data = parser::parse_python_resample_from_local_file_call(_py, data);
    let mut runtime = tokio::runtime::Runtime::new().unwrap();
    let result = runtime.block_on(execute_resample_save_file_from_local_file(parsed_data));
    Ok(result)
}

pub fn resample_save_file_from_url(_py: Python, data: PyObject) -> PyResult<bool> {
    let parsed_data = parser::parse_python_resample_from_file_url_call(_py, data);
    let mut runtime = tokio::runtime::Runtime::new().unwrap();
    let result = runtime.block_on(execute_resample_save_file_from_url(parsed_data));
    Ok(result)
}


pub fn render(_py: Python, data: PyObject) -> PyResult<String> {
    let mut trace = TraceItem::new(String::from("render"));

    let trace_initialization = trace.create_child(String::from("Initialization"));
    let parsed_data = parser::parse_python_render_call(_py, data);
    let expected_render_file_hash = hasher::hash(&parsed_data);

    let mut runtime = tokio::runtime::Runtime::new().unwrap();

    let engine_base_s3_url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com";
    let expected_render_url = format!(
        "{}/{}/{}/files/{}.mp3",
        engine_base_s3_url,
        parsed_data.engine_account_id.borrow().as_ref().unwrap(),
        parsed_data.engine_project_id.borrow().as_ref().unwrap(),
        expected_render_file_hash
    );
    trace_initialization.close();

    let trace_check_matching_file_exist = trace.create_child(String::from("Check matching file already exist"));
    let file_exist = runtime.block_on(loader::file_exist_at_url(&*expected_render_url));
    trace_check_matching_file_exist.close();

    if file_exist == true {
        trace.close();
        Ok(expected_render_url)
    } else {
        let file_url = runtime.block_on(append::main(&mut trace, parsed_data, expected_render_file_hash))
            .expect("Append future did not returned a valid file_url");
        trace.close();
        Ok(file_url.unwrap_or(String::from("null")))
    }
}
