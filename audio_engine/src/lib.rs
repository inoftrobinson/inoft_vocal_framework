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
#[path="tests/mod.rs"] pub mod tests;

use std::borrow::Borrow;
use crate::resampler::resample;
use std::fs::File;
use std::path::Path;
use std::io::Write;
use crate::tracer::TraceItem;
use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject};
use crate::models::ResampleSaveFileReceivedParsedData;


py_module_initializer!(audio_engine, |py, m| {
    m.add(py, "__doc__", "Render dynamic audio.")?;
    m.add(py, "resample_save_file_from_url", py_fn!(py, resample_save_file_from_url(data: PyObject)))?;
    m.add(py, "render", py_fn!(py, render(data: PyObject)))?;
    Ok(())
});


pub async fn ex(data: ResampleSaveFileReceivedParsedData) -> bool {
    let trace = &mut TraceItem::new(String::from("Ex"));

    let (samples, codec_params) = decoder::decode_from_file_url(
        trace, &*data.file_url, 0.0, None
    ).await;

    let source_filename = data.file_url.split("/").last().unwrap();
    let source_file_extension = source_filename.split(".").last().unwrap();
    let filename_with_wav_extension = source_filename.replacen(source_file_extension, "wav", 1);
    let expected_efs_filepath = format!("{}/{}", data.target_dirpath, filename_with_wav_extension);

    // /mnt/files/

    let target_spec = hound::WavSpec {
        channels: 1,
        sample_rate: 48000,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };
    let resamples = resample(trace, samples.unwrap(), codec_params.unwrap(), target_spec);

    let mut writer =  hound::WavWriter::create(expected_efs_filepath, target_spec).unwrap();
    for sample in resamples {
        writer.write_sample(sample).unwrap();
    }

    trace.close();
    true
}

pub fn resample_save_file_from_url(_py: Python, data: PyObject) -> PyResult<bool> {
    let parsed_data = parser::parse_python_resample_call(_py, data);
    let mut runtime = tokio::runtime::Runtime::new().unwrap();
    let result = runtime.block_on(ex(parsed_data));
    Ok(result)
}


pub fn render(_py: Python, data: PyObject) -> PyResult<String> {
    let parsed_data = parser::parse_python_render_call(_py, data);
    let expected_render_file_hash = hasher::hash(&parsed_data);
    println!("expected_render_file_hash : {}", expected_render_file_hash);

    let mut runtime = tokio::runtime::Runtime::new().unwrap();

    let engine_base_s3_url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com";
    let expected_render_url = format!(
        "{}/{}/{}/files/{}.mp3",
        engine_base_s3_url,
        parsed_data.engine_account_id.borrow().as_ref().unwrap(),
        parsed_data.engine_project_id.borrow().as_ref().unwrap(),
        expected_render_file_hash
    );
    let file_exist = runtime.block_on(loader::file_exist_at_url(&*expected_render_url));
    if file_exist == true {
        Ok(expected_render_url)
    } else {
        let file_url = runtime.block_on(append::main(parsed_data, expected_render_file_hash))
            .expect("Append future did not returned a valid file_url");
        Ok(file_url.unwrap_or(String::from("null")))
    }
}
