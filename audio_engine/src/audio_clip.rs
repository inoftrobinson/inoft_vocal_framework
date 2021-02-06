use hound::{WavReader, WavSpec, WavSamples};
use std::io::{BufReader};
use std::fs::File;
use crate::resampler::{resample_i16, resample_i32};
use crate::models::Time;
use std::cell::RefCell;
use crate::loader::get_file_bytes_from_url;
use std::any::Any;
use std::{io, fs};
use bytes::Bytes;
use tokio::macros::support::Future;
use serde::{Serialize, Deserialize};
use std::borrow::Borrow;


// todo: remove the passing and loading of clip ids ?
pub struct AudioClip {
    pub clip_id: String,
    pub filepath: Option<String>,
    pub file_url: Option<String>,
    pub volume: Option<u8>,
    pub player_start_time: Time,
    pub player_end_time: Time,
    pub file_start_time: i16,
    pub file_end_time: i16,
    pub resamples: Option<Vec<i16>>,
    player_start_time_sample_index: Option<usize>,
    player_end_time_sample_index: Option<usize>,
}


impl AudioClip {
    pub fn new(clip_id: String, filepath: Option<String>, file_url: Option<String>, volume: Option<u8>,
               player_start_time: Time, player_end_time: Time, file_start_time: i16, file_end_time: i16) -> RefCell<AudioClip> {
        RefCell::new(AudioClip {
            clip_id, filepath, file_url, volume,
            player_start_time, player_end_time,
            file_start_time, file_end_time,
            resamples: None,
            player_start_time_sample_index: None,
            player_end_time_sample_index: None
        })
    }

    fn make_resamples<R: io::Read>(mut wave_reader: WavReader<R>, target_spec: WavSpec) -> Option<Vec<i16>> {
        let reader_spec = wave_reader.spec();
        let mut resamples: Option<Vec<i16>> = None;
        if reader_spec.bits_per_sample <= 16 {
            let samples= wave_reader.samples();
            resamples = Some(resample_i16(samples, reader_spec, target_spec));
        } else if reader_spec.bits_per_sample <= 32 {
            let samples = wave_reader.samples();
            resamples = Some(resample_i32(samples, reader_spec, target_spec));
        } else {
            panic!("Bits per sample superior to 32 is not supported");
        }
        resamples
    }

    pub async fn resample(&mut self, target_spec: WavSpec) {
        if self.file_url.is_none() != true {
            let bytes = get_file_bytes_from_url(&*self.file_url.as_ref().unwrap()).await;
            let mut bytes_reader: WavReader<BufReader<&[u8]>> = WavReader::new(BufReader::new(&*bytes)).unwrap();
            self.resamples = AudioClip::make_resamples(bytes_reader, target_spec);
        } else {
            let filepath = self.filepath.as_ref().unwrap();
            let mut file_reader = WavReader::open(filepath).unwrap();
            self.resamples = AudioClip::make_resamples(file_reader, target_spec);
        }
    }

    pub fn render_player_start_time_to_sample_index(&mut self, target_sample_rate: u32) -> usize {
        self.player_start_time_sample_index = Some((self.player_start_time.offset.unwrap_or(0) as i32 * target_sample_rate as i32) as usize);
        self.player_start_time_sample_index.unwrap()
    }

    pub fn render_player_end_time_to_sample_index(&mut self, target_sample_rate: u32) -> usize {
        if self.player_end_time_sample_index.is_none() {
            self.render_player_start_time_to_sample_index(target_sample_rate);
        }
        let type_key = &*self.player_end_time.type_key;
        let index_end_sample: usize = match type_key {
            "until-self-end" => {
                self.resamples.as_ref().expect("The 'resample' function has not been called.").len()
            },
            _ => {
                panic!("Unsupported type_key {}", type_key);
            }
        };
        index_end_sample + self.player_start_time_sample_index.unwrap()
    }
}
