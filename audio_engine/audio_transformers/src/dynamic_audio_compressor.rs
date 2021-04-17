use hound::WavSpec;
use crate::base_transformer::BaseTransformer;


pub struct DynamicAudioCompressorSettings {

}

impl DynamicAudioCompressorSettings {
    pub fn new(
        parent_renderer_target_wav_spec: &WavSpec
    ) -> DynamicAudioCompressorSettings {
        let sample_rate = parent_renderer_target_wav_spec.sample_rate as f64;
        DynamicAudioCompressorSettings {
        }
    }
}


pub struct DynamicAudioCompressor {
    active_peak_index: usize,
    active_peak_value: f32,
    settings: DynamicAudioCompressorSettings,
}

impl DynamicAudioCompressor {
    pub fn new(parent_renderer_target_wav_spec: &WavSpec) -> DynamicAudioCompressor {
        DynamicAudioCompressor {
            active_peak_index: 0,
            active_peak_value: f32::MIN,
            settings: DynamicAudioCompressorSettings::new(
                parent_renderer_target_wav_spec,
            )
        }
    }
}

impl BaseTransformer<i16> for DynamicAudioCompressor {
    fn should_run(&mut self) -> bool {
        false
    }

    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16 {
        sample_value
        /*let floated_sample_value = sample_value as f32;
        if floated_sample_value > self.active_peak_value {
            self.active_peak_index = sample_index;
            self.active_peak_value = floated_sample_value;
        } else {
            if sample_index > (self.active_peak_index + (self.settings.attack_time_in_samples + self.settings.hold_time_in_samples)) {
                self.active_peak_index = sample_index;
                self.active_peak_value = floated_sample_value;
            }
        }

        let current_value_threshold = self.calculate_max_value_threshold(sample_index);
        // println!("current_value_threshold : {}", current_value_threshold);
        if floated_sample_value > 0.0 {
            if floated_sample_value > current_value_threshold {
                let value_above_threshold = floated_sample_value - current_value_threshold;
                sample_value - ((value_above_threshold / self.settings.compression_ratio) as i16)
            } else {
                sample_value
            }
        } else {
            let current_value_negative_threshold = -current_value_threshold;
            if floated_sample_value < current_value_negative_threshold {
                let value_below_threshold = current_value_negative_threshold - floated_sample_value;
                sample_value + ((value_below_threshold / self.settings.compression_ratio) as i16)
            } else {
                sample_value
            }
        }*/
    }
}