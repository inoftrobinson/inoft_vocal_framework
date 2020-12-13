extern crate cpython;
mod append;
mod resampler;
mod renderer;
mod exporter;
pub mod parser;
mod models;
use models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, Time};
mod tests;
mod audio_clip;
use audio_clip::AudioClip;


use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject};

py_module_initializer!(inoft_audio_engine_renderer, |py, m| {
    m.add(py, "__doc__", "Render dynamic audio.")?;
    m.add(py, "render", py_fn!(py, render(data: PyObject)))?;
    Ok(())
});

pub fn render(_py: Python, data: PyObject) -> PyResult<String> {
    let parsed_data = parser::parse_python(_py, data);
    // exporter::from_flac_to_mp3();
    append::main(parsed_data);
    Ok(String::from("https://inoft.com"))
}
