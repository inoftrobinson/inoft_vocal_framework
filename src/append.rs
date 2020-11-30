// Hound -- A wav encoding and decoding library in Rust
// Copyright 2018 Ruud van Asseldonk
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// A copy of the License has been included in the root of the repository.
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This example appends one second of a 440 Hz sine wave to the file "sine.wav".
// If the file does not exist, it is created instead.

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
use crate::resampler::resample;

extern crate hound;

pub fn main() {
    let spec = hound::WavSpec {
        channels: 1,
        sample_rate: 44100,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };
    let expected_spec = hound::WavSpec {
        channels: 2,
        sample_rate: 44100,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };

    let path: &Path = "F:/Sons utiles/output_dummy.wav".as_ref();
    let mut writer = match path.is_file() {
        true => hound::WavWriter::append(path).unwrap(),
        false => hound::WavWriter::create(path, expected_spec).unwrap(),
    };

    // We should not append blindly, we should make sure that the existing file
    // has the right spec, because that is what we assume when writing.
    println!("{:?}", writer.spec());
    assert_eq!(expected_spec, writer.spec());

    println!("Old duration is {} seconds.", writer.duration() / spec.sample_rate);

    let mut files_readers: Vec<WavReader<BufReader<File>>> = vec![];
    // let files_paths: Vec<&str> = vec!["F:/Sons utiles/sine.wav", "F:/Sons utiles/ambiance.wav"];
    let files_paths: Vec<&str> = vec!["F:/Sons utiles/out_0.wav", "F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav"];  // "F:/Sons utiles/out_1.wav"];
    let mut duration_longest_file_buffer: u32 = 0;
    let mut file_reader_longest_file: Option<WavReader<BufReader<File>>> = None;
    let mut file_reader_longest_file_2: Option<&WavReader<BufReader<File>>> = None;

    if files_paths.len() > 0 {
        for (i, filepath) in files_paths.iter().enumerate() {
            let filepath = files_paths[i];
            let mut file_reader = WavReader::open(filepath).unwrap();
            let sample_rate = file_reader.spec().sample_rate as i32;

            let samples: WavSamples<BufReader<File>, i16> = file_reader.samples();
            let resamples = resample(samples, sample_rate, 44100);
            for i in 0..resamples.len() {
                writer.write_sample(resamples[i]).unwrap();
            }

            files_readers.push(file_reader);
            let mut current_file_reader = &files_readers[i];

            println!("current spec = {:?}", current_file_reader.spec());
            if current_file_reader.spec().sample_rate != expected_spec.sample_rate {
                println!("Converting file with ffmpeg...");

                let mut out_filepath = String::new();
                out_filepath.push_str("F:/Sons utiles/out_");
                out_filepath.push_str(&i.to_string());
                out_filepath.push_str(".wav");

                let sound: std::process::Output = Command::new("ffmpeg")
                    .arg("-i").arg(filepath)
                    .arg("-sample_rate").arg("44100")
                    .arg("-y").arg(out_filepath)
                    .stdout(Stdio::piped())
                    .stdin(Stdio::inherit())
                    .stderr(Stdio::inherit())
                    .output()
                    .unwrap();

                files_readers[i] = WavReader::open("F:/Sons utiles/ambiance_out.wav").unwrap();
                current_file_reader = &files_readers[i];
            }

            println!("{}", current_file_reader.duration());
            println!("{:?}", current_file_reader.spec());
            let current_file_duration = current_file_reader.duration();
            if current_file_duration > duration_longest_file_buffer {
                duration_longest_file_buffer = current_file_duration;
                file_reader_longest_file_2 = Some(current_file_reader);
            }
        }
        // println!("{}", duration_longest_file_buffer / file_reader_longest_file_2.unwrap().spec().sample_rate);
        // let samples: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
        let samples1: Vec<i16> = files_readers[0].samples().map(|s| s.unwrap()).collect();
        /*let samples2: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
        println!("spec : {:?}", files_readers[0].spec());
        // println!("{:?}", samples2);

        for samp in samples2.iter() {
            let amplitude = i16::MAX as i16;
            let value = if samp > &amplitude { &amplitude } else { samp };
            // writer.write_sample((samp * amplitude) as i32).unwrap();
            writer.write_sample((value * 1) as i16);  // .unwrap();
        }
         */

        /*for s in samples.iter() {
            let amplitude = i16::MAX as i16;
            writer.write_sample((s * amplitude) as i16).unwrap();
        }*/

        /*for filereader in files_readers.iter() {
            let samples: WavSamples<BufReader<File>, <Unknown>> = filereader.samples();  //.map(|s| s.unwrap()).collect();
            /*for sample in samples.iter() {
                println!("{}", sample);
            }*/
        }*/

        /*for t in (0 .. 44100).map(|x| x as f32 / 44100.0) {
            let sample = (t * 440.0 * 2.0 * PI).sin();
            let amplitude = i16::MAX as f32;
            writer.write_sample((sample * amplitude as f32) as i16).unwrap();
        }*/
    }

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


    /*let mut reader = WavReader::open("F:/Sons utiles/sine.wav").unwrap();
    let mut reader2 = WavReader::open("F:/Sons utiles/ambiance.wav").unwrap();
    reader2.duration()
    let samples: Vec<i16> = reader.samples().map(|s| s.unwrap()).collect();
    for sample in samples.iter() {
        println!("{:?}", sample);
        let m =  sample * 1;
        println!("{:?}", m);
    }
     */
        /*(0.0, |sqr_sum, s| {
        let sample = s.unwrap() as f64;
        // println!("{}", sample);
        sqr_sum + sample * sample;
        sqr_sum
    });
         */

    /*
    for t in (0 .. 44100).map(|x| x as f32 / 44100.0) {
        let sample = (t * 440.0 * 2.0 * PI).sin();
        let amplitude = i16::MAX as f32;
        writer.write_sample((sample * amplitude as f32) as i16).unwrap();
    }
     */

    println!("New duration is {} seconds.", writer.duration() / spec.sample_rate);

    writer.finalize().unwrap();
}