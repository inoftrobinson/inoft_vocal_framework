use hound::{WavSpec};
use std::io;
use symphonia::core::codecs::CodecParameters;
use crate::tracer::TraceItem;


fn resample_sample_rate_without_channels_conversion(samples: Vec<i16>, resample_interval: f32) -> Vec<i16> {
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;
    for (i, sample) in samples.iter().enumerate() {
        let float_index = i as f32;
        while float_index > resample_count {
            out_samples.push(*sample);
            resample_count += resample_interval;
        }
    }
    out_samples
}

fn resample_sample_rate_and_channels_from_one_to_two(samples: Vec<i16>, resample_interval: f32) -> Vec<i16> {
    // This function is almost exactly like the resample_sample_rate_without_channels_conversion function.
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;
    for (i, sample) in samples.iter().enumerate() {
        let sample_value = *sample;
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

fn resample_sample_rate_and_channels_from_two_to_one(samples: Vec<i16>, resample_interval: f32) -> Vec<i16> {
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;

    let num_samples_unique_across_channels = samples.len() / 2;
    let mut samples_enumerator = samples.iter().enumerate();
    for i in 0..num_samples_unique_across_channels {
        let float_index = i as f32;
        // A WAV file with 2 channels is represented like [240, 240, 102, 102, 720, 720].
        let channel_one_sample_data = samples_enumerator.next().unwrap().1;
        let channel_two_sample_data = samples_enumerator.next().unwrap().1;
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

fn print_resampling_starting(source_num_samples: usize, source_sample_rate: u32, target_sample_rate: u32, resample_interval: f32, bits_divider: Option<f32>) {
    println!(
        "\nResampling starting...\
        \n  --source_num_samples:{}\
        \n  --source_sample_rate:{}\
        \n  --target_sample_rate:{}\
        \n  --resample_interval:{}\
        \n  --bits_divider:{}",
        source_num_samples, source_sample_rate,
        target_sample_rate, resample_interval,
        bits_divider.unwrap_or(1.0)
    );
}

fn print_resampling_completed(execution_time: u128, num_returned_samples: usize) {
    println!(
        "\nResampling completed.\
        \n  --execution_time:{}ms\
        \n  --num_returned_samples:{}",
        execution_time, num_returned_samples
    );
}

fn panic_source_num_channels_not_supported(source_num_channels: u16) {
    panic!(
        "The num of audio channels in your source file is not supported.\
        \nOnly audio files with 1 or 2 audio channels are supported.\
        \n  --source_spec.channels:{}", source_num_channels
    );
}

fn panic_target_num_channels_not_supported(target_num_channels: u16) {
    panic!(
        "The num of audio channels that you are targeting to resample to is not supported.\
        \nOnly targeting to 1 or 2 audio channels is supported.\
        --target_spec.channels:{}", target_num_channels
    );
}


// The resampler can handle 4 different channels conversions :
// source 1 -> target 1 (handled by resample_sample_rate_without_channels_conversion)
// source 1 -> target 2 (handled by resample_sample_rate_and_channels_from_two_to_one)
// source 2 -> target 2 (handled by resample_sample_rate_without_channels_conversion)
// source 2 -> target 1 (handled by resample_sample_rate_and_channels_from_one_to_two)
// Any other scenario will cause the resampler to panic.

pub fn resample(trace: &mut TraceItem, samples: Vec<i16>, source_spec: CodecParameters, target_spec: WavSpec) -> Vec<i16> {
    let trace_initialization = trace.create_child(String::from("initialization"));
    let source_sample_rate = source_spec.sample_rate.unwrap();
    let source_num_channels = source_spec.channels.unwrap().count() as u16;
    let source_bits_per_sample = source_spec.bits_per_sample.unwrap_or(16) as u16;
    let target_sample_rate = target_spec.sample_rate;
    trace_initialization.close();

    if source_sample_rate == target_spec.sample_rate && source_num_channels == target_spec.channels && source_bits_per_sample == target_spec.bits_per_sample {
        samples
    } else {
        let trace_resampling = trace.create_child(String::from("resampling"));
        let resample_interval = source_sample_rate as f32 / target_sample_rate as f32;
        print_resampling_starting(samples.len(), source_sample_rate, target_sample_rate, resample_interval, None);

        let mut handler: Option<fn(Vec<i16>, f32) -> Vec<i16>> = None;
        if target_spec.channels == 1 {
            if source_num_channels == 1 {
                handler = Some(resample_sample_rate_without_channels_conversion);
            } else if source_num_channels == 2 {
                handler = Some(resample_sample_rate_and_channels_from_two_to_one);
            } else {
                panic_source_num_channels_not_supported(source_num_channels);
            }
        } else if target_spec.channels == 2 {
            if source_num_channels == 2 {
                handler = Some(resample_sample_rate_without_channels_conversion);
            } else if source_num_channels == 1 {
                handler = Some(resample_sample_rate_and_channels_from_one_to_two);
            } else {
                panic_source_num_channels_not_supported(source_num_channels);
            }
        } else {
            panic_target_num_channels_not_supported(target_spec.channels);
        }
        let out_samples = handler.unwrap()(samples, resample_interval);
        trace_resampling.close();
        print_resampling_completed(trace_resampling.elapsed, out_samples.len());
        out_samples
    }
}