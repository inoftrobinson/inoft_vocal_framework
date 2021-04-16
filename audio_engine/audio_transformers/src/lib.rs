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

fn make_wave_spec_from_audio_buffer(audio_buffer: &AudioBuffer) -> WavSpec {
    WavSpec {
        channels: audio_buffer.number_of_channels() as u16,
        sample_rate: audio_buffer.sample_rate() as u32,
        bits_per_sample: 16,  // todo: remove hardcoded value
        sample_format: SampleFormat::Float
    }
}

fn apply_transformer(audio_buffer: AudioBuffer, wav_spec: WavSpec, mut transformer_instance: Box<dyn BaseTransformer>) {
    if transformer_instance.should_run() {
        for channel_index in 0..wav_spec.channels {
            // If you are wondering why we use u32 for the get_channel_data and i32 for copy_to_channel,
            // it's not a mistake in the audio engine, simply what the AudioBuffer api dumbly expect.
            let current_channel_data: Result<Vec<f32>, JsValue> = audio_buffer.get_channel_data(channel_index as u32);
            match current_channel_data {
                Ok(mut sample_data) => {
                    for i_sample in 0..sample_data.len() {
                        sample_data[i_sample] = transformer_instance.alter_sample(sample_data[i_sample], i_sample);
                    }
                    audio_buffer.copy_to_channel(sample_data.as_slice(), channel_index as i32);
                }
                Err(js_value) => {
                    alert("Rust error my man");
                    alert(&*js_value.as_string().unwrap());
                }
            }
        }
    }
}

#[wasm_bindgen]
pub fn apply_tremolo(audio_buffer: AudioBuffer, speed: f32, gain: f32) {
    let wav_spec = make_wave_spec_from_audio_buffer(&audio_buffer);
    let mut tremolo_transformer = Tremolo::new(&wav_spec, speed, gain);
    apply_transformer(audio_buffer, wav_spec, Box::new(tremolo_transformer));
}