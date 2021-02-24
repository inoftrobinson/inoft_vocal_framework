use std::cell::RefCell;
use hound::{WavReader, WavSpec, WavSamples, WavIntoSamples, SampleFormat, WavWriter};
use crate::resampler::{resample};
use crate::models::Time;
use crate::decoder;
use crate::tracer::TraceItem;

// todo: do a benchmark comparison between WavHound and symphonia for opening WavFiles


// todo: remove the passing and loading of clip ids ?
pub struct AudioClip {
    pub clip_id: String,
    pub filepath: Option<String>,
    pub file_url: Option<String>,
    pub volume: Option<u8>,
    pub player_start_time: Time,
    pub player_end_time: Time,
    pub file_start_time: f32,
    pub file_end_time: Option<f32>,
    pub resamples: Option<Vec<i16>>,
    player_start_time_sample_index: Option<usize>,
    player_end_time_sample_index: Option<usize>,
}


impl AudioClip {
    pub fn new(clip_id: String, filepath: Option<String>, file_url: Option<String>, volume: Option<u8>,
               player_start_time: Time, player_end_time: Time, file_start_time: f32, file_end_time: Option<f32>) -> RefCell<AudioClip> {
        RefCell::new(AudioClip {
            clip_id, filepath, file_url, volume,
            player_start_time, player_end_time,
            file_start_time, file_end_time,
            resamples: None,
            player_start_time_sample_index: None,
            player_end_time_sample_index: None,
        })
    }

    pub fn generate_random_bytes(len: usize) -> Box<[u8]> {
        let mut lcg: u32 = 0xec57c4bf;
        let mut bytes = vec![0; len];
        for quad in bytes.chunks_mut(4) {
            lcg = lcg.wrapping_mul(1664525).wrapping_add(1013904223);
            for (src, dest) in quad.iter_mut().zip(&lcg.to_ne_bytes()) {
                *src = *dest;
            }
        }
        bytes.into_boxed_slice()
    }

    pub async fn resample(&mut self, trace: &mut TraceItem, target_spec: WavSpec, limit_time_to_load: Option<f32>) {
        let (samples, codec_params) = if self.file_url.is_none() != true {
            let trace_decoding_from_file_url = trace.create_child(String::from("Decoding from file url"));
            let file_url = self.file_url.as_ref().unwrap();
            let (samples, codec_params) = decoder::decode_from_file_url(
                trace_decoding_from_file_url, file_url, self.file_start_time, limit_time_to_load
            ).await;
            trace_decoding_from_file_url.close();
            (samples, codec_params)
        } else {
            let trace_decoding_from_local_filepath = trace.create_child(String::from("Decoding from local filepath"));
            let filepath = self.filepath.as_ref().unwrap();
            let (samples, codec_params) = decoder::decode_from_local_filepath(
                trace_decoding_from_local_filepath, filepath, self.file_start_time, limit_time_to_load
            );
            trace_decoding_from_local_filepath.close();
            (samples, codec_params)
        };

        let trace_make_resamples = trace.create_child(String::from("Make resamples"));
        self.resamples = Some(resample(trace_make_resamples, samples.unwrap(), codec_params.unwrap(), target_spec));
        trace_make_resamples.close();
    }

    pub fn render_player_start_time_to_sample_index(&mut self, target_sample_rate: u32) -> usize {
        self.player_start_time_sample_index = Some((self.player_start_time.offset.unwrap_or(0.0) * target_sample_rate as f32) as usize);
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
