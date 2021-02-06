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

use audio_clip::AudioClip;


use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject, ObjectProtocol};

py_module_initializer!(audio_engine, |py, m| {
    m.add(py, "__doc__", "Render dynamic audio.")?;
    m.add(py, "render", py_fn!(py, render(data: PyObject)))?;
    Ok(())
});


pub fn render(_py: Python, data: PyObject) -> PyResult<String> {
    let parsed_data = parser::parse_python(_py, data);
    let mut runtime = tokio::runtime::Runtime::new().unwrap();
    let file_url = runtime.block_on(append::main(parsed_data));
    Ok(file_url.unwrap_or(String::from("null")))
}