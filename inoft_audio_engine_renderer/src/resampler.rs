use hound::{WavSpec};
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::time::{Instant};
use std::io;


fn i16_resample_sample_rate_without_channels_conversion<R: io::Read>(samples: WavSamples<R, i16>, resample_interval: f32) -> Vec<i16> {
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

fn i32_resample_sample_rate_without_channels_conversion<R: io::Read>(samples: WavSamples<R, i32>, resample_interval: f32, bits_divider: f32) -> Vec<i16> {
    // For comments, see i16_resample_sample_rate_without_channels_conversion
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;
    for (i, sample) in samples.enumerate() {
        let sample_value = ((sample.unwrap() as f32) / bits_divider) as i16;
        let float_index = i as f32;
        while float_index > resample_count {
            out_samples.push(sample_value);
            resample_count += resample_interval;
        }
    }
    out_samples
}

fn i16_resample_sample_rate_and_channels_from_one_to_two<R: io::Read>(samples: WavSamples<R, i16>, resample_interval: f32) -> Vec<i16> {
    // This function is almost exactly like the i16_resample_sample_rate_without_channels_conversion function.
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

fn i32_resample_sample_rate_and_channels_from_one_to_two<R: io::Read>(samples: WavSamples<R, i32>, resample_interval: f32, bits_divider: f32) -> Vec<i16> {
    // For comments, see i16_resample_sample_rate_and_channels_from_one_to_two
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;
    for (i, sample) in samples.enumerate() {
        let sample_value = ((sample.unwrap() as f32) / bits_divider) as i16;
        let float_index = i as f32;
        while float_index > resample_count {
            out_samples.push(sample_value);
            out_samples.push(sample_value);
            resample_count += resample_interval;
        }
    }
    out_samples
}


fn i16_resample_sample_rate_and_channels_from_two_to_one<R: io::Read>(samples: WavSamples<R, i16>, resample_interval: f32) -> Vec<i16> {
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

fn i32_resample_sample_rate_channels_and_from_two_to_one<R: io::Read>(samples: WavSamples<R, i32>, resample_interval: f32, bits_divider: f32) -> Vec<i16> {
    // For comments, see i16_resample_sample_rate_and_channels_from_two_to_one
    let mut out_samples: Vec<i16> = Vec::new();
    let mut resample_count: f32 = 0.0;

    let num_samples_unique_across_channels = samples.len() / 2;
    let mut samples_enumerator = samples.enumerate();
    for i in 0..num_samples_unique_across_channels {
        let float_index = i as f32;
        let channel_one_sample_data = samples_enumerator.next().unwrap().1.unwrap();
        let channel_two_sample_data = samples_enumerator.next().unwrap().1.unwrap();
        let sample_value = ((((channel_one_sample_data / 2) + (channel_two_sample_data / 2)) as f32) / bits_divider) as i16;
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
// source 1 -> target 1 (handled by i16_resample_sample_rate_without_channels_conversion)
// source 1 -> target 2 (handled by i16_resample_sample_rate_and_channels_from_two_to_one)
// source 2 -> target 2 (handled by i16_resample_sample_rate_without_channels_conversion)
// source 2 -> target 1 (handled by i16_resample_sample_rate_and_channels_from_one_to_two)
// Any other scenario will cause the resampler to panic.

pub fn resample_i16<R: io::Read>(samples: WavSamples<R, i16>, source_spec: WavSpec, target_spec: WavSpec) -> Vec<i16> {
    let source_sample_rate = source_spec.sample_rate;
    let target_sample_rate = target_spec.sample_rate;

    if source_spec.sample_rate == target_spec.sample_rate && source_spec.channels == target_spec.channels && source_spec.bits_per_sample == target_spec.bits_per_sample {
        samples.map(|s| s.unwrap()).collect()
    } else {
        let resample_interval = source_sample_rate as f32 / target_sample_rate as f32;
        let resample_start = Instant::now();
        print_resampling_starting(samples.len(), source_sample_rate, target_sample_rate, resample_interval, None);

        let mut handler: Option<fn(WavSamples<R, i16>, f32) -> Vec<i16>> = None;
        if target_spec.channels == 1 {
            if source_spec.channels == 1 {
                handler = Some(i16_resample_sample_rate_without_channels_conversion);
            } else if source_spec.channels == 2 {
                handler = Some(i16_resample_sample_rate_and_channels_from_two_to_one);
            } else {
                panic_source_num_channels_not_supported(source_spec.channels);
            }
        } else if target_spec.channels == 2 {
            if source_spec.channels == 2 {
                handler = Some(i16_resample_sample_rate_without_channels_conversion);
            } else if source_spec.channels == 1 {
                handler = Some(i16_resample_sample_rate_and_channels_from_one_to_two);
            } else {
                panic_source_num_channels_not_supported(source_spec.channels);
            }
        } else {
            panic_target_num_channels_not_supported(target_spec.channels);
        }
        let out_samples = handler.unwrap()(samples, resample_interval);
        print_resampling_completed(resample_start.elapsed().as_millis(), out_samples.len());
        out_samples
    }
}

pub fn resample_i32<R: io::Read>(samples: WavSamples<R, i32>, source_spec: WavSpec, target_spec: WavSpec) -> Vec<i16> {
    let source_sample_rate = source_spec.sample_rate;
    let target_sample_rate = target_spec.sample_rate;

    let resample_interval = source_sample_rate as f32 / target_sample_rate as f32;
    let bits_divider = (source_spec.bits_per_sample as f32 / target_spec.bits_per_sample as f32) * 256.0;
    // todo: document why we need to multiply the divider by 256 (honestly, i do not know why 256 exactly, but it works, so...)
    let resample_start = Instant::now();
    print_resampling_starting(samples.len(), source_sample_rate, target_sample_rate, resample_interval, Some(bits_divider));

    // The audio engine is made to handle 16 bits data, so if the resample_i32 function is called, we now for sure that we need
    // to resample. We do not even need to do a comparison of the source spec and target spec like in the resample_i16 function.
    let mut handler: Option<fn(WavSamples<R, i32>, f32, f32) -> Vec<i16>> = None;
    if target_spec.channels == 1 {
        if source_spec.channels == 1 {
            handler = Some(i32_resample_sample_rate_without_channels_conversion);
        } else if source_spec.channels == 2 {
            handler = Some(i32_resample_sample_rate_channels_and_from_two_to_one);
        } else {
            panic_source_num_channels_not_supported(source_spec.channels);
        }
    } else if target_spec.channels == 2 {
        if source_spec.channels == 2 {
            handler = Some(i32_resample_sample_rate_without_channels_conversion);
        } else if source_spec.channels == 1 {
            handler = Some(i32_resample_sample_rate_and_channels_from_one_to_two);
        } else {
            panic_source_num_channels_not_supported(source_spec.channels);
        }
    } else {
        panic_target_num_channels_not_supported(target_spec.channels);
    }
    let out_samples = handler.unwrap()(samples, resample_interval, bits_divider);
    print_resampling_completed(resample_start.elapsed().as_millis(), out_samples.len());
    out_samples
}