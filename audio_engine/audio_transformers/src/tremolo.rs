use hound::WavSpec;
use crate::base_transformer::BaseTransformer;
use crate::generators::sinewave::Sinewave;


pub struct TremoloSettings {
    speed: f32,
    gain: f32
}

impl TremoloSettings {
    pub fn new(parent_renderer_target_wav_spec: &WavSpec, speed: f32, gain: f32) -> TremoloSettings {
        TremoloSettings {
            speed, gain
        }
    }
}


pub struct Tremolo {
    active_peak_index: usize,
    active_peak_value: f32,
    settings: TremoloSettings,
    sinewave_generator: Sinewave
}

impl Tremolo {
    pub fn new(parent_renderer_target_wav_spec: &WavSpec) -> Tremolo {
        Tremolo {
            active_peak_index: 0,
            active_peak_value: f32::MIN,
            settings: TremoloSettings::new(
                parent_renderer_target_wav_spec,
                3.0, 0.9
            ),
            // todo: convert speed to a sinewave frequency
            sinewave_generator: Sinewave::new(44100.0, 20.0)
        }
    }
}

impl BaseTransformer for Tremolo {
    fn alter_sample(&mut self, sample_value: f32, sample_index: usize) -> f32 {
        let sine_value = self.sinewave_generator.make_sample(sample_index);
        let sine_absolute = (1.0 + sine_value) / 2.0;
        let volume = 1.0 - (self.settings.gain * sine_absolute);
        sample_value * volume
    }
}