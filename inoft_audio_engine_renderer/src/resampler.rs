use hound::{WavReader, WavSpec};
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::time::{Instant};
use std::borrow::{Borrow, BorrowMut};
use std::num::Wrapping;


fn resample_sample_rate_without_channels_conversion(samples: WavSamples<BufReader<File>, i16>, resample_interval: f32) -> Vec<i16> {
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;
    for (i, sample) in samples.enumerate() {
        let sample_value = sample.unwrap();
        let float_index = i as f32;
        while float_index > resample_count {
            out_samples.push(sample_value);
            resample_count += resample_interval;
        }
    }
    out_samples
}

fn resample_sample_rate_and_channels_from_one_to_two(samples: WavSamples<BufReader<File>, i16>, resample_interval: f32) -> Vec<i16> {
    // This function is almost exactly like the resample_sample_rate_without_channels_conversion function.
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;
    for (i, sample) in samples.enumerate() {
        let sample_value = sample.unwrap();
        let float_index = i as f32;
        while float_index > resample_count {
            // To change the channel from one to two, we just need to add twice the sample_value to the out_samples.
            // Because a WAV file with 2 channels is represented like [240, 240, 102, 102, 720, 720], where the
            // first two samples are played together as the same sample, but coming from different channels.
            out_samples.push(sample_value);
            out_samples.push(sample_value);
            resample_count += resample_interval;
        }
    }
    out_samples
}

fn resample_sample_rate_and_channels_from_two_to_one(samples: WavSamples<BufReader<File>, i16>, resample_interval: f32) -> Vec<i16> {
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;

    let num_samples_unique_across_channels = samples.len() / 2;
    let mut samples_enumerator = samples.enumerate();
    for i in 0..num_samples_unique_across_channels {
        let float_index = i as f32;
        // A WAV file with 2 channels is represented like [240, 240, 102, 102, 720, 720].
        let channel_one_sample_data = samples_enumerator.next().unwrap().1.unwrap();
        let channel_two_sample_data = samples_enumerator.next().unwrap().1.unwrap();
        // So, since this function only support conversion from two channels to one, we can simply use an
        // iterator twice, to get the sample value both in the first channel, and in the second channel.
        let sample_value = (channel_one_sample_data / 2) + (channel_two_sample_data / 2);
        // And then add them together, by dividing them separately, instead of dividing them once they have been
        // added, to avoid overflow issues when they have been added before they have been divided. Of course, it
        // cost us two divisions instead of one, but it free us from a type conversion from i16 to something like i32.
        while float_index > resample_count {
            out_samples.push(sample_value);
            resample_count += resample_interval;
        }
    }
    out_samples
}



pub fn resample(samples: WavSamples<BufReader<File>, i16>, source_spec: WavSpec, target_spec: WavSpec) -> Vec<i16> {
    // todo: add resampling for bitsize

    let source_sample_rate = source_spec.sample_rate;
    let target_sample_rate = target_spec.sample_rate;

    if source_spec.sample_rate == target_spec.sample_rate && source_spec.channels == target_spec.channels {
        samples.map(|s| s.unwrap()).collect()
    } else {
        let resample_interval = source_sample_rate as f32 / target_sample_rate as f32;
        let resample_start = Instant::now();
        println!(
            "\nResampling starting...\n  --source_num_samples:{}\n  --source_sample_rate:{}\n  --target_sample_rate:{}\n  --resample_interval:{}",
            samples.len(), source_sample_rate, target_sample_rate, resample_interval
        );

        // The resampler can handle 4 different channels conversions :
        // source 1 -> target 1 (handled by resample_sample_rate_without_channels_conversion)
        // source 1 -> target 2 (handled by resample_sample_rate_and_channels_from_two_to_one)
        // source 2 -> target 2 (handled by resample_sample_rate_without_channels_conversion)
        // source 2 -> target 1 (handled by resample_sample_rate_and_channels_from_one_to_two)
        // Any other scenario will cause the resampler to panic.
        let mut handler: Option<fn(WavSamples<BufReader<File>, i16>, f32) -> Vec<i16>> = None;
        if target_spec.channels == 1 {
            if source_spec.channels == 1 {
                handler = Some(resample_sample_rate_without_channels_conversion);
            } else if source_spec.channels == 2 {
                handler = Some(resample_sample_rate_and_channels_from_two_to_one);
            } else {
                panic!(
                    "The num of audio channels in your source file is not supported.\
                    \nOnly audio files with 1 or 2 audio channels are supported.\
                    \n  --source_spec.channels:{}", source_spec.channels
                );
            }
        } else if target_spec.channels == 2 {
            if source_spec.channels == 2 {
                handler = Some(resample_sample_rate_without_channels_conversion);
            } else if source_spec.channels == 1 {
                handler = Some(resample_sample_rate_and_channels_from_one_to_two);
            } else {
                panic!(
                    "The num of audio channels in your source file is not supported.\
                    \nOnly audio files with 1 or 2 audio channels are supported.\
                    \n  --source_spec.channels:{}", source_spec.channels
                );
            }
        } else {
            panic!(
                "The num of audio channels that you are targeting to resample to is not supported.\
                \nOnly targeting to 1 or 2 audio channels is supported.\
                --target_spec.channels:{}", target_spec.channels
            );
        }
        let out_samples = handler.unwrap()(samples, resample_interval);
        println!(
            "\nResampling completed.\n  --execution_time:{}ms\n  --num_returned_samples:{}",
            resample_start.elapsed().as_millis(), out_samples.len()
        );
        out_samples
    }
}