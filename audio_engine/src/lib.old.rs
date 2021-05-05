extern crate cpython;
/*mod libs;
use libs::hound2;
 */
#[path="append.rs"] mod append;
use append::main;
#[path="resampler.rs"] pub mod resampler;
#[path="renderer.rs"] pub mod renderer;
#[path="exporter.rs"] pub mod exporter;
#[path="parser.rs"] pub mod parser;
#[path="models.rs"] mod models;
use models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, Time};
#[path="audio_clip.rs"] mod audio_clip;
#[path="loader.rs"] pub mod loader;
#[path="hasher.rs"] pub mod hasher;
#[path="tests/mod.rs"] pub mod tests;

use audio_clip::AudioClip;


use std::time::Instant;
use std::borrow::Borrow;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn string_sum(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;

    Ok(())
}

/*

pub fn render(_py: Python, data: PyAny) -> PyResult<String> {
    let parsed_data = parser::parse_python(_py, data);
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

 */