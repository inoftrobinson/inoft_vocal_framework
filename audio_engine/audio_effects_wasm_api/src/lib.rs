mod applicator;

use wasm_bindgen::prelude::*;
use web_sys::AudioBuffer;
use audio_transformers::tremolo::Tremolo;
use crate::applicator::{apply_effect, make_wave_spec_from_audio_buffer};


#[wasm_bindgen]
extern {
    pub fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}!", name));
}

#[wasm_bindgen]
pub fn apply_tremolo(audio_buffer: AudioBuffer, speed: f32, gain: f32) {
    let wav_spec = make_wave_spec_from_audio_buffer(&audio_buffer);
    // &wav_spec,
    let mut tremolo_transformer = Tremolo::new(speed, gain);
    apply_effect(audio_buffer, wav_spec, Box::new(tremolo_transformer));
}