use crate::base_transformer::BaseTransformer;
use crate::generators::sinewave::Sinewave;


pub struct TremoloSettings {
    speed: f32,
    gain: f32
}

impl TremoloSettings {
    // parent_renderer_target_wav_spec: &WavSpec,
    pub fn new(speed: f32, gain: f32) -> TremoloSettings {
        TremoloSettings {
            speed, gain
        }
    }
}


pub struct Tremolo {
    settings: TremoloSettings,
    sinewave_generator: Sinewave
}

impl Tremolo {
    // parent_renderer_target_wav_spec: &WavSpec,
    pub fn new(speed: f32, gain: f32) -> Tremolo {
        Tremolo {
            // parent_renderer_target_wav_spec
            settings: TremoloSettings::new(speed, gain),
            sinewave_generator: Sinewave::new(44100.0, speed)
        }
    }

    fn compute_volume(&self, sample_index: usize) -> f32 {
        let sine_value = self.sinewave_generator.make_sample(sample_index);
        let sine_absolute = (1.0 + sine_value) / 2.0;
        let volume = 1.0 - (self.settings.gain * sine_absolute);
        volume
    }
}

impl BaseTransformer<f32> for Tremolo {
    fn should_run(&mut self) -> bool {
        self.settings.gain > 0.0 && self.settings.speed > 0.0
    }

    fn alter_sample(&mut self, sample_value: f32, sample_index: usize) -> f32 {
        sample_value * self.compute_volume(sample_index)
    }
}

impl BaseTransformer<i16> for Tremolo {
    fn should_run(&mut self) -> bool {
        self.settings.gain > 0.0 && self.settings.speed > 0.0
    }

    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16 {
        (sample_value as f32 * self.compute_volume(sample_index)) as i16
    }
}