mod applicator;

use wasm_bindgen::prelude::*;
use web_sys::AudioBuffer;
use audio_effects::tremolo::Tremolo;
use crate::applicator::{apply_effect, make_wave_spec_from_audio_buffer};
use audio_effects::equalizer::{EqualizerTransformer, CurveItemData};


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


#[wasm_bindgen]
pub fn apply_equalizer(audio_buffer: AudioBuffer, curves: &JsValue) {
    // let elements: Vec<CurveItemData> = curves.into_serde().unwrap();

    let wav_spec = make_wave_spec_from_audio_buffer(&audio_buffer);
    let mut equalizer_transformer = EqualizerTransformer::new(vec![]);
    /*
            equalizer.set(0, Curve::Highpass, 100.0, 0.5f64.sqrt(), -10.0);
        equalizer.set(1, Curve::Lowpass, 20000.0, 10.0, -12.0);
     */
    apply_effect(audio_buffer, wav_spec, Box::new(equalizer_transformer));
}