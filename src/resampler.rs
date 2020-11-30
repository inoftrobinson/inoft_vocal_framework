use hound::WavReader;
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::time::{Instant};


pub fn resample(samples: WavSamples<BufReader<File>, i16>, source_sample_rate: i32, target_sample_rate: i32) -> Vec<i16> {
    if source_sample_rate == target_sample_rate {
        samples.map(|s| s.unwrap()).collect()
    } else {
        let mut out_samples: Vec<i16> = Vec::new();
        let mut resample_count: i32 = 0;
        let resample_interval = source_sample_rate / target_sample_rate;

        let resample_start = Instant::now();
        for (i, sample) in samples.enumerate() {
            if i as i32 > resample_count {
                out_samples.push(sample.unwrap());
                resample_count += resample_interval;
            }
        }
        println!("Resampler took {}s to execute.", resample_start.elapsed().as_secs());
        out_samples
    }
}