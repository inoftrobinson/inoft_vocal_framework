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
use std::time::Instant;
use self::hound::WavSpec;
use std::num::Wrapping;

extern crate hound;

const TARGET_SPEC: WavSpec = hound::WavSpec {
    channels: 1,
    sample_rate: 16000,
    bits_per_sample: 16,
    sample_format: hound::SampleFormat::Int,
};


pub struct AudioClip {
    filepath: String,
    player_start_time: i16,
    player_end_time: i16,
    file_start_time: i16,
    file_end_time: i16,
}

impl AudioClip {
    fn new(filepath: &str, player_start_time: Option<i16>, player_end_time: Option<i16>,
           file_start_time: Option<i16>, file_end_time: Option<i16>) -> AudioClip {
        AudioClip {
            filepath: String::from(filepath),
            player_start_time: player_start_time.unwrap_or(0),
            player_end_time: player_end_time.unwrap_or(0),
            file_start_time: file_start_time.unwrap_or(0),
            file_end_time: file_end_time.unwrap_or(0)
        }
    }

    fn without_args(filepath: &str) -> AudioClip {
        AudioClip::new(filepath, None, None, None, None)
    }
}


pub fn main() {
    let start = Instant::now();
    let path: &Path = "F:/Sons utiles/output_dummy_2.wav".as_ref();
    /*let mut writer = match path.is_file() {
        true => hound::WavWriter::append(path).unwrap(),
        false => hound::WavWriter::create(path, TARGET_SPEC).unwrap(),
    };*/

    let mut files_readers: Vec<WavReader<BufReader<File>>> = vec![];
    let files_paths: Vec<AudioClip> = vec![
        // AudioClip::without_args("F:/Inoft/anvers_1944_project/inoft_vocal_engine/speech_synthesis/export/builtin_text-wqhtNB/final_render.wav"),
        // AudioClip::without_args("F:/Inoft/anvers_1944_project/inoft_vocal_engine/speech_synthesis/export/builtin_text-wqhtNB/final_render.wav"),
        // AudioClip::without_args("F:/Inoft/anvers_1944_project/inoft_vocal_engine/speech_synthesis/export/builtin_text-VOcldO/final_render.wav"),
        AudioClip::without_args("F:/Sons utiles/ambiance_out.wav"),
        AudioClip::without_args("F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav"),
        AudioClip::new(
            "F:/Inoft/anvers_1944_project/inoft_vocal_engine/speech_synthesis/export/builtin_text-nVXWAn/final_render.wav",
            Some(20), None, None, None
        ),
    ];
    let mut duration_longest_file_buffer: u32 = 0;
    let mut file_reader_longest_file: Option<&WavReader<BufReader<File>>> = None;

    if files_paths.len() > 0 {
        let mut out_samples: Vec<i16> = Vec::new();
        for (i_file, filepath) in files_paths.iter().enumerate() {
            let audio_clip = &files_paths[i_file];
            let filepath = &audio_clip.filepath;
            let mut file_reader = WavReader::open(filepath).unwrap();
            println!("spec : {:?}", file_reader.spec());

            let sample_rate = file_reader.spec().sample_rate as i32;
            let samples: WavSamples<BufReader<File>, i16> = file_reader.samples();
            let resamples = resample(samples, sample_rate, TARGET_SPEC.sample_rate as i32);

            let outing_start = Instant::now();
            let start_sample = (audio_clip.player_start_time as i32 * TARGET_SPEC.sample_rate as i32) as usize;
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

        println!("out samples : {}", out_samples.len());
        let mut writer =  hound::WavWriter::create(path, TARGET_SPEC).unwrap();
        let writing_start = Instant::now();
        for i_sample in 0..out_samples.len() {
            writer.write_sample(out_samples[i_sample]).unwrap();
        }
        println!("\nFinished writing.\n  --execution_time:{}ms", writing_start.elapsed().as_millis());
        // writer.finalize().unwrap();



        /*for (i_reader, mut file_reader) in files_readers.iter().enumerate() {
            let sample_rate = file_reader.spec().sample_rate as i32;
            let samples: WavSamples<BufReader<File>, i16> = file_reader.samples();
            let resamples = resample(samples, sample_rate, TARGET_SPEC.sample_rate as i32);
            for i_sample in 0..resamples.len() {
                writer.write_sample(resamples[i_sample]).unwrap();
            }
        }
         */
        // println!("{}", duration_longest_file_buffer / file_reader_longest_file.unwrap().spec().sample_rate);
        // let samples: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
        // let samples1: Vec<i16> = files_readers[0].samples().map(|s| s.unwrap()).collect();
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

    println!("Total execution time : {}ms", start.elapsed().as_millis());
}