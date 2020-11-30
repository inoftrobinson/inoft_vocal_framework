@@ -1,130 +0,0 @@
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

use std::ptr;
use std::f32::consts::PI;
use std::i16;
use std::path::Path;
use hound::WavReader;
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::ptr::null;

extern crate hound;

pub fn main() {
    let spec = hound::WavSpec {
        channels: 1,
        sample_rate: 44100,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };

    let path: &Path = "F:/Sons utiles/output_dummy.wav".as_ref();
    let mut writer = match path.is_file() {
        true => hound::WavWriter::append(path).unwrap(),
        false => hound::WavWriter::create(path, spec).unwrap(),
    };

    // We should not append blindly, we should make sure that the existing file
    // has the right spec, because that is what we assume when writing.
    println!("{:?}", writer.spec());
    assert_eq!(spec, writer.spec());

    println!("Old duration is {} seconds.", writer.duration() / spec.sample_rate);

    let mut files_readers: Vec<WavReader<BufReader<File>>> = vec![];
    let files_paths: Vec<&str> = vec!["F:/Sons utiles/sine.wav", "F:/Sons utiles/ambiance.wav"];
    let mut duration_longest_file_buffer: u32 = 0;
    let mut file_reader_longest_file: Option<WavReader<BufReader<File>>> = None;
    let mut file_reader_longest_file_2: Option<&WavReader<BufReader<File>>> = None;

    if files_paths.len() > 0 {
        for filepath in files_paths.iter() {
            files_readers.push(WavReader::open(filepath).unwrap());
            file_reader_longest_file_2 = Some(&files_readers[0]);
        }
        for filereader in files_readers.iter() {
            println!("{}", filereader.duration());
            let current_file_duration = filereader.duration();
            if current_file_duration > duration_longest_file_buffer {
                duration_longest_file_buffer = current_file_duration;
                file_reader_longest_file_2 = Some(filereader);
            }
        }
        // println!("{}", duration_longest_file_buffer / file_reader_longest_file_2.unwrap().spec().sample_rate);

        /*for filereader in files_readers.iter() {
            let samples: WavSamples<BufReader<File>, <Unknown>> = filereader.samples();  //.map(|s| s.unwrap()).collect();
            /*for sample in samples.iter() {
                println!("{}", sample);
            }*/
        }*/

        for t in (0 .. 44100).map(|x| x as f32 / 44100.0) {
            let sample = (t * 440.0 * 2.0 * PI).sin();
            let amplitude = i16::MAX as f32;
            writer.write_sample((sample * amplitude as f32) as i16).unwrap();
        }
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