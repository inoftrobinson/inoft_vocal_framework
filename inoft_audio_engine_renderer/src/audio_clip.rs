use hound::{WavReader, WavSpec, WavSamples};
use std::io::BufReader;
use std::fs::File;
use crate::resampler::{resample_i16, resample_i32};
use crate::models::Time;
use std::cell::RefCell;

pub struct AudioClip {
    pub clip_id: String,
    pub filepath: Option<String>,
    pub file_url: Option<String>,
    pub player_start_time: Time,
    pub player_end_time: Time,
    pub file_start_time: i16,
    pub file_end_time: i16,
    pub resamples: Option<Vec<i16>>,
    player_start_time_sample_index: Option<usize>,
    player_end_time_sample_index: Option<usize>,
}

impl AudioClip {
    pub fn new(clip_id: String, filepath: Option<String>, file_url: Option<String>,
               player_start_time: Time, player_end_time: Time, file_start_time: i16, file_end_time: i16) -> RefCell<AudioClip> {
        RefCell::new(AudioClip {
            clip_id, filepath, file_url,
            player_start_time, player_end_time,
            file_start_time, file_end_time,
            resamples: None,
            player_start_time_sample_index: None,
            player_end_time_sample_index: None
        })
    }

    pub fn resample(&mut self, target_spec: WavSpec) { // -> &Vec<i16> {
        // todo: check if the filepath is specified or the fileurl
        let filepath = self.filepath.as_ref().unwrap();
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
        self.resamples = Some(resamples.unwrap());
        // &self.resamples.unwrap()
    }

    pub fn render_player_start_time_to_sample_index(&mut self, target_sample_rate: u32) -> usize {
        self.player_start_time_sample_index = Some((self.player_start_time.offset.unwrap_or(0) as i32 * target_sample_rate as i32) as usize);
        self.player_start_time_sample_index.unwrap()
    }

    pub fn render_player_end_time_to_sample_index(&mut self, target_sample_rate: u32) -> usize {
        if self.player_end_time_sample_index.is_none() {
            self.render_player_start_time_to_sample_index(target_sample_rate);
        }
        let index_end_sample: usize = match &*self.player_end_time.type_key {
            "until-self-end" => {
                self.resamples.as_ref().expect("The 'resample' function has not been called.").len()
            },
            _ => {
                panic!("Unsupported type_key");
            }
        };
        index_end_sample + self.player_start_time_sample_index.unwrap()
    }
}
