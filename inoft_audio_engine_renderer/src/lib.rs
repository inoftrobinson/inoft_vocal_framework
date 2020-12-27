extern crate cpython;
/*mod libs;
use libs::hound2;
 */
mod append;
use append::main;
mod resampler;
mod renderer;
mod exporter;
pub mod parser;
use parser::parse_python;
mod models;
use models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, Time};
mod tests;
mod audio_clip;
mod loader;

use audio_clip::AudioClip;


use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject, ObjectProtocol};

py_module_initializer!(inoft_audio_engine_renderer, |py, m| {
    m.add(py, "__doc__", "Render dynamic audio.")?;
    m.add(py, "render", py_fn!(py, render(data: PyObject)))?;
    Ok(())
});

/*
pub async fn execute_render() {
    let task_1 = tokio::spawn(exporter::get_upload_url(String::from("test.mp3"), 1000));
        let task_2 = tokio::spawn(append::main(data));
        let tasks = tokio::join!(task_1, task_2);
        println!("Finished tokio...");
}
 */

pub fn render(_py: Python, data: PyObject) -> PyResult<String> {
    let parsed_data = parser::parse_python(_py, data);
    let mut runtime = tokio::runtime::Runtime::new().unwrap();
    runtime.block_on(append::main(parsed_data));
    Ok(String::from("https://inoft.com"))
}