extern crate cpython;
mod append;
use append::{AudioBlock, AudioClip, Track};
mod resampler;
mod renderer;
mod exporter;
pub mod parser;
mod models;
use models::{ReceivedParsedData, ReceivedTargetSpec};


use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject, ObjectProtocol};

py_module_initializer!(inoft_audio_engine_renderer, |py, m| {
    m.add(py, "__doc__", "This module is implemented in Rust.")?;
    m.add(py, "render", py_fn!(py, render(data: PyObject)))?;
    Ok(())
});

fn render(_py: Python, data: PyObject) -> PyResult<String> {
    let audio_clips = parser::parse_python(_py, data);
    // println!("{:?}", audio_blocks_data.get_item(_py, "start"));
    // todo: retrieve the AudioClips objects from Python
    // exporter::from_flac_to_mp3();
    append::main(audio_clips);
    Ok((String::from("https://inoft.com")))
}