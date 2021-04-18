use crate::base_transformer::BaseTransformer;
use crate::generators::sinewave::Sinewave;
use crate::equalizer::equalizer::Equalizer;
use crate::equalizer::design::Curve;
use serde::{Serialize, Deserialize};


#[derive(Serialize, Deserialize)]
pub struct CurveItemData {
    curve: String,
    gain: f32,
    frequency: f32,
    resonance: f32,
}


pub struct EqualizerSettings {
}

impl EqualizerSettings {
    // parent_renderer_target_wav_spec: &WavSpec,
    pub fn new() -> EqualizerSettings {
        EqualizerSettings {
        }
    }
}


pub struct EqualizerTransformer {
    settings: EqualizerSettings,
    equalizer: Equalizer<f64>
}

impl EqualizerTransformer {
    pub fn new(curves: Vec<CurveItemData>) -> EqualizerTransformer {
        let mut equalizer = Equalizer::new(48.0e3);
        equalizer.set(0, Curve::Highpass, 100.0, 0.5f64.sqrt(), -10.0);
        equalizer.set(1, Curve::Lowpass, 20000.0, 10.0, -12.0);
        EqualizerTransformer { settings: EqualizerSettings::new(), equalizer }
    }
}

impl BaseTransformer<f32> for EqualizerTransformer {
    fn should_run(&mut self) -> bool {
        true
    }

    fn alter_sample(&mut self, sample_value: f32, sample_index: usize) -> f32 {
        // sample_value * self.compute_volume(sample_index)
        self.equalizer.process(sample_value as f64) as f32
    }
}

impl BaseTransformer<i16> for EqualizerTransformer {
    fn should_run(&mut self) -> bool {
        true
    }

    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16 {
        self.equalizer.process(sample_value as f64) as i16
    }
}
