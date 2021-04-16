use hound::WavSpec;
use crate::transformers::base_transformer::BaseTransformer;


pub struct AudioCompressorSettings {
    compression_ratio: f32,
    attack_time_in_ms: f64,
    hold_time_in_ms: f64,
    release_time_in_ms: f64,
    decibels_threshold: f32,
    attack_time_in_samples: usize,
    hold_time_in_samples: usize,
    release_time_in_samples: usize,
    max_value_negative_threshold: f32,
}

impl AudioCompressorSettings {
    pub fn new(
        parent_renderer_target_wav_spec: &WavSpec, compression_ratio: f32, attack_time_in_ms: f64,
        hold_time_in_ms: f64, release_time_in_ms: f64, decibels_threshold: f32
    ) -> AudioCompressorSettings {
        let sample_rate = parent_renderer_target_wav_spec.sample_rate as f64;
        let amplitude_threshold =  (-decibels_threshold) / 90.0;
        AudioCompressorSettings {
            compression_ratio, attack_time_in_ms, hold_time_in_ms, release_time_in_ms, decibels_threshold,
            attack_time_in_samples: (sample_rate * (attack_time_in_ms / 1000.0)) as usize,
            hold_time_in_samples: (sample_rate * (hold_time_in_ms / 1000.0)) as usize,
            release_time_in_samples: (sample_rate * (release_time_in_ms / 1000.0)) as usize,
            max_value_negative_threshold: i16::MAX as f32 - (amplitude_threshold * i16::MAX as f32)
        }
    }
}


pub struct AudioCompressor {
    active_peak_index: usize,
    active_peak_value: f32,
    settings: AudioCompressorSettings,
}

impl AudioCompressor {
    pub fn new(parent_renderer_target_wav_spec: &WavSpec) -> AudioCompressor {
        AudioCompressor {
            active_peak_index: 0,
            active_peak_value: f32::MIN,
            settings: AudioCompressorSettings::new(
                parent_renderer_target_wav_spec,
                2.0,
                82.0,
                1000.0,
                1400.0,
                -25.0
            )
        }
    }

    fn calculate_max_value_threshold(&self, sample_index: usize) -> f32 {
        let num_samples_since_reached_peaked = sample_index - self.active_peak_index;

        if self.settings.attack_time_in_samples >= num_samples_since_reached_peaked {
            // Attack is in progress
            let attack_position = num_samples_since_reached_peaked as f32 / self.settings.attack_time_in_samples as f32;
            (self.settings.max_value_negative_threshold * attack_position) + (self.active_peak_value * (1.0 - attack_position))
            // We weight more the max_value_threshold more and more the oldest the peak becomes, and we we
            // weight more the active_peak_value the more recent it is. This will create a linear curve
            // behavior, where we will gradually reduce the gain after a peak, relative to the peak value.
        } else if (self.settings.attack_time_in_samples + self.settings.release_time_in_samples) >= num_samples_since_reached_peaked {
            // Release is in progress
            let num_samples_since_start_release = num_samples_since_reached_peaked - self.settings.attack_time_in_samples;
            let release_position = num_samples_since_start_release as f32 / self.settings.release_time_in_samples as f32;
            (self.settings.max_value_negative_threshold * (1.0 - release_position)) + (self.active_peak_value * release_position)
        } else {
            // Neither attack or release are in progress
            self.settings.max_value_negative_threshold
            // When neither attack or the release are in progress, we just return the max_value_threshold as our
            // current_value_threshold. Computing the value as if the attack was still in progress could result in a
            // negative value, when doing a (1.0 - attack_position), since the attack position will be greater than 1.
        }
    }
}

impl BaseTransformer for AudioCompressor {
    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16 {
        let floated_sample_value = sample_value as f32;
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
        }
    }
}