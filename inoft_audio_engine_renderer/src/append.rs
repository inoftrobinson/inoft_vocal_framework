use std::{ptr, process};
use std::f32::consts::PI;
use std::i16;
use std::path::Path;
use hound::WavReader;
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::ptr::null;
use std::borrow::Borrow;
use std::process::{Command, Stdio};
use crate::resampler::{resample_i16, resample_i32};
use std::time::Instant;
use self::hound::WavSpec;
use std::num::Wrapping;
use crate::{ReceivedParsedData, ReceivedTargetSpec};
use crate::exporter::{from_samples_to_mono_mp3, write_mp3_buffer_to_file};

extern crate hound;


pub fn render_to_vec(data: &ReceivedParsedData) -> Vec<i16> {
    let start = Instant::now();

    let mut out_samples: Vec<i16> = Vec::new();
    let mut files_readers: Vec<WavReader<BufReader<File>>> = vec![];
    let mut duration_longest_file_buffer: u32 = 0;
    let mut file_reader_longest_file: Option<&WavReader<BufReader<File>>> = None;

    // The inoft_audio_engine_renderer has been optimized and tested to render audio with 16 bits per sample.
    // Changing this value to 24 (the only other possible setting), could cause unexpected behaviors.
    let target_spec = hound::WavSpec {
        channels: 1,
        sample_rate: data.target_spec.sample_rate as u32,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };

    if data.blocks.len() > 0 {
        let first_audio_block = data.blocks.get(0).unwrap();
        let first_track = first_audio_block.tracks.get(0).unwrap();
        let audio_clips = &first_track.clips;
        // todo: fix that and support multiple audio blocks instead of just using the first one

        for (i_file, filepath) in audio_clips.iter().enumerate() {
            let audio_clip = &audio_clips[i_file];
            let filepath = &audio_clip.filepath;
            println!("file : {}", filepath);
            let mut file_reader = WavReader::open(filepath).unwrap();
            println!("spec : {:?}", file_reader.spec());

            let file_reader_spec = file_reader.spec();
            let mut resamples: Option<Vec<i16>> = None;
            if file_reader_spec.bits_per_sample <= 16 {
                let samples: WavSamples<BufReader<File>, i16> = file_reader.samples();
                resamples = Some(resample_i16(samples, file_reader_spec, target_spec));
            } else if file_reader_spec.bits_per_sample <= 32 {
                let samples: WavSamples<BufReader<File>, i32> = file_reader.samples();
                resamples = Some(resample_i32(samples, file_reader_spec, target_spec));
            } else {
                panic!("Bits per sample superior to 32 is not supported");
            }
            let resamples = resamples.unwrap();

            let outing_start = Instant::now();
            let start_sample = (audio_clip.player_start_time as i32 * data.target_spec.sample_rate as i32) as usize;
            println!("start_sample = {}", start_sample);
            for i_sample in 0..resamples.len() {
                // todo: fix issue where if the first sound has a player_start_time more than
                //  zero, it will be pushed in the out_samples like if it had no player_start_time.
                let current_sample_index = i_sample + start_sample;
                if out_samples.len() > current_sample_index + 1 {
                    out_samples[current_sample_index] = (Wrapping(out_samples[current_sample_index]) + Wrapping(resamples[i_sample])).0;
                } else {
                    out_samples.push(resamples[i_sample]);
                }
            }
            println!("\nFinished outing.\n  --execution_time:{}ms", outing_start.elapsed().as_millis());

            /*
            files_readers.push(file_reader);
            let mut current_file_reader = &files_readers[i_file];

            println!("current spec = {:?}", current_file_reader.spec());
            println!("{}", current_file_reader.duration());
            println!("{:?}", current_file_reader.spec());
            let current_file_duration = current_file_reader.duration();
            if current_file_duration > duration_longest_file_buffer {
                duration_longest_file_buffer = current_file_duration;
                file_reader_longest_file = Some(current_file_reader);
            }
             */
        }
    }

    println!("Total rendering time : {}ms", start.elapsed().as_millis());
    out_samples
}

pub fn main(data: ReceivedParsedData) {
    let start = Instant::now();
    let path: &Path = data.target_spec.filepath.as_ref();
    let target_spec = &data.target_spec;
    let rendered_samples = render_to_vec(&data);

    let writing_start = Instant::now();
    match &*target_spec.format_type {
        "mp3" => {
            write_mp3_buffer_to_file(from_samples_to_mono_mp3(rendered_samples, target_spec), &*target_spec.filepath);
        },
        "wav" => {
            let wav_target_spec = hound::WavSpec {
                channels: 1,
                sample_rate: target_spec.sample_rate as u32,
                bits_per_sample: 16,
                sample_format: hound::SampleFormat::Int,
            };
            let mut writer =  hound::WavWriter::create(path, wav_target_spec).unwrap();
            for i_sample in 0..rendered_samples.len() {
                writer.write_sample(rendered_samples[i_sample]).unwrap();
            }
        },
        _ => {
            panic!(
                "Format type not supported. Only 'mp3' and 'wav' formats are supported to export audio.\
                \n  --request_format_type:{}", target_spec.format_type
            );
        }
    }
    println!("\nFinished conversion and writing.\n  --execution_time:{}ms", writing_start.elapsed().as_millis());
    println!("\nFinished rendering, conversion and writing.\n  --execution_time:{}ms", start.elapsed().as_millis());
    // writer.finalize().unwrap();

    /*for (i_reader, mut file_reader) in files_readers.iter().enumerate() {
        let sample_rate = file_reader.spec().sample_rate as i32;
        let samples: WavSamples<BufReader<File>, i16> = file_reader.samples();
        let resamples = resample(samples, sample_rate, TARGET_SPEC.sample_rate as i32);
        for i_sample in 0..resamples.len() {
            writer.write_sample(resamples[i_sample]).unwrap();
        }
    }
    // println!("{}", duration_longest_file_buffer / file_reader_longest_file.unwrap().spec().sample_rate);
    // let samples: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
    // let samples1: Vec<i16> = files_readers[0].samples().map(|s| s.unwrap()).collect();
    let samples2: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
    println!("spec : {:?}", files_readers[0].spec());
    // println!("{:?}", samples2);
     */

    /*
    if files_paths.len() > 0 {
        for filepath in files_paths.iter() {
            let current_file_reader = WavReader::open(filepath).unwrap();

            let current_file_duration = current_file_reader.duration();
            if current_file_duration > duration_longest_file_buffer {
                duration_longest_file_buffer = current_file_duration;
                file_reader_longest_file = Some(current_file_reader);
            }
            // files_readers.push(current_file_reader);
        }
        // println!("{}", duration_longest_file_buffer / file_reader_longest_file.unwrap().spec().sample_rate);
    }
    */
}