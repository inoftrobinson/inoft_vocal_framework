extern crate cpython;
mod append;
use append::AudioClip;
mod resampler;
mod renderer;

use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject, ObjectProtocol};

py_module_initializer!(inoft_audio_engine_renderer, |py, m| {
    m.add(py, "__doc__", "This module is implemented in Rust.")?;
    m.add(py, "get_result", py_fn!(py, get_result(val: &str, audio_clip: PyObject)))?;
    Ok(())
});

fn get_result(_py: Python, val: &str, audio_clip: PyObject) -> PyResult<String> {
    println!("{:?}", audio_clip);
    println!("{:?}", audio_clip.get_item(_py, "start"));
    append::main();
    Ok("Rust says: ".to_owned() + val)
}