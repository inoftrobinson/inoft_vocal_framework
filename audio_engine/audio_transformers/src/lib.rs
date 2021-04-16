pub mod generators;
mod base_transformer;
mod tremolo;

use wasm_bindgen::prelude::*;
use js_sys::Float32Array;
use web_sys::AudioBuffer;
use crate::tremolo::Tremolo;
use hound::{WavSpec, SampleFormat};
use crate::base_transformer::BaseTransformer;
use std::num::Wrapping;


#[wasm_bindgen]
extern {
    pub fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}!", name));
}

#[wasm_bindgen]
pub fn apply_tremolo(audio_buffer: AudioBuffer) {
    // alert(&format!("Running the tremolo on the data {}", audio_buffer.duration()));

    let wav_spec = WavSpec {
        channels: audio_buffer.number_of_channels() as u16,
        sample_rate: audio_buffer.sample_rate() as u32,
        bits_per_sample: 16,  // todo: remove hardcoded value
        sample_format: SampleFormat::Float
    };
    let mut tremolo = Tremolo::new(&wav_spec);
    let first_channel_data: Result<Vec<f32>, JsValue> = audio_buffer.get_channel_data(0);
    match first_channel_data {
        Ok(mut sample_data) => {
            for i_sample in 0..sample_data.len() {
                sample_data[i_sample] = tremolo.alter_sample(sample_data[i_sample], i_sample);
            }
            /*for i_sample in 0..sample_data.len() {
                sample_data[i_sample] = Wrapping(sample_data[i_sample] * 2.0).0;
            }*/
            audio_buffer.copy_to_channel(sample_data.as_slice(), 0);
        }
        Err(js_value) => {
            alert("Rust error my man");
            alert(&*js_value.as_string().unwrap());
        }
    }

    if wav_spec.channels > 1 {
        let second_channel_data: Result<Vec<f32>, JsValue> = audio_buffer.get_channel_data(1);
        match second_channel_data {
            Ok(mut sample_data) => {
                for i_sample in 0..sample_data.len() {
                    sample_data[i_sample] = tremolo.alter_sample(sample_data[i_sample], i_sample) as f32;
                }
                audio_buffer.copy_to_channel(sample_data.as_slice(), 1);
            }
            Err(js_value) => {
                alert("Rust error my man");
                alert(&*js_value.as_string().unwrap());
            }
        }
    }
}