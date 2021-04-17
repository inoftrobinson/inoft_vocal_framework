use hound::WavSpec;
use crate::transformers::base_transformer::BaseTransformer;
use std::f32::consts::PI;
use crate::generators::sinewave::Sinewave;


pub struct BallerSettings {
    speed: f32,
    gain: f32
}

impl BallerSettings {
    pub fn new(parent_renderer_target_wav_spec: &WavSpec, speed: f32, gain: f32) -> BallerSettings {
        BallerSettings {
            speed, gain
        }
    }
}


pub struct Baller {
    settings: BallerSettings,
    sinewave: Sinewave
}

impl Baller {
    pub fn new(parent_renderer_target_wav_spec: &WavSpec) -> Baller {
        Baller {
            settings: BallerSettings::new(
                parent_renderer_target_wav_spec,
                3.0, 0.5
            ),
            sinewave: Sinewave::new(44100.0, 500.0)
        }
    }
}

impl BaseTransformer for Baller {
    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16 {
        let sine_value = self.sinewave.make_sample(sample_index);
        let volume = self.settings.gain * sine_value;
        (sample_value as f32 * volume) as i16
    }
}