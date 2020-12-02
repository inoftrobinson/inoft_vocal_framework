use hound::WavReader;
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::time::{Instant};


pub fn resample(samples: WavSamples<BufReader<File>, i16>, source_sample_rate: i32, target_sample_rate: i32) -> Vec<i16> {
    // todo: add resampling for num of channels, and for bitsize

    if source_sample_rate == target_sample_rate {
        samples.map(|s| s.unwrap()).collect()
    } else {
        let mut out_samples: Vec<i16> = Vec::new();
        let mut resample_count: f32 = 0.0;
        let resample_interval = source_sample_rate as f32 / target_sample_rate as f32;

        println!(
            "\nResampling starting...\n  --source_num_samples:{}\n  --source_sample_rate:{}\n  --target_sample_rate:{}\n  --resample_interval:{}",
            samples.len(), source_sample_rate, target_sample_rate, resample_interval
        );
        let resample_start = Instant::now();

        for (i, sample) in samples.enumerate() {
            let sample_value = sample.unwrap();
            let float_index = i as f32;
            while float_index > resample_count {
                out_samples.push(sample_value);
                resample_count += resample_interval;
            }
        }
        println!("\nResampling completed.\n  --execution_time:{}ms\n  --num_returned_samples:{}", resample_start.elapsed().as_millis(), out_samples.len());
        out_samples
    }
}