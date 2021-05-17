use std::cell::RefCell;
use hound::{WavSpec};
use crate::resampler::{resample};
use crate::models::{Time, EngineApiData};
use crate::{decoder, engine_api_client};
use crate::tracer::TraceItem;
use std::borrow::Borrow;
use audio_effects::base_transformer::BaseTransformer;
use bytes::Bytes;

// todo: do a benchmark comparison between WavHound and symphonia for opening WavFiles


// todo: remove the passing and loading of clip ids ?
pub struct AudioClip {
    pub clip_id: String,
    pub clip_type: String,
    pub file_bytes: Option<Vec<u8>>,
    pub filepath: Option<String>,
    pub file_url: Option<String>,
    pub text: Option<String>,
    pub voice_key: Option<String>,
    pub volume: Option<u16>,
    pub effects: RefCell<Vec<Box<dyn BaseTransformer<i16>>>>,
    pub player_start_time: Time,
    pub player_end_time: Time,
    pub file_start_time: f32,
    pub file_end_time: Option<f32>,
    pub resamples: Option<Vec<i16>>,
    player_start_time_sample_index: Option<usize>,
    player_end_time_sample_index: Option<usize>,
}


impl AudioClip {
    pub fn new(
        clip_id: String, clip_type: String,
        file_bytes: Option<Vec<u8>>, filepath: Option<String>, file_url: Option<String>,
        text: Option<String>, voice_key: Option<String>,
        volume: Option<u16>, effects: Vec<Box<dyn BaseTransformer<i16>>>,
        player_start_time: Time, player_end_time: Time, file_start_time: f32, file_end_time: Option<f32>
    ) -> RefCell<AudioClip> {
        RefCell::new(AudioClip {
            clip_id, clip_type,
            file_bytes, filepath, file_url,
            text, voice_key,
            volume, effects: RefCell::new(effects),
            player_start_time, player_end_time,
            file_start_time, file_end_time,
            resamples: None,
            player_start_time_sample_index: None,
            player_end_time_sample_index: None,
        })
    }

    pub async fn resample(&mut self, trace: &mut TraceItem, engine_api_data: &EngineApiData, target_spec: WavSpec, limit_time_to_load: Option<f32>) {

        let (samples, codec_params) = match self.clip_type.as_str() {
            // The order of the if statements below are not picked at random ! In case for some reasons multiple file data
            // protocol have been passed to this audio clip (file_bytes, filepath or file_url), we will try to load the first
            // cheapest protocol. The cheapest is loading from bytes, then loading from filepath, and finally loading from file url.
            "file" => {
                if self.file_bytes.is_none() != true {
                    let trace_decoding_from_bytes = trace.create_child(String::from("Decoding from bytes"));
                    let boxed_file_bytes = self.file_bytes.as_ref().unwrap().clone().into_boxed_slice();
                    let (samples, codec_params) = decoder::decode_from_bytes(
                        trace_decoding_from_bytes, boxed_file_bytes, String::from("mp3"), self.file_start_time, limit_time_to_load
                    );
                    // todo: make file extension dynamic
                    trace_decoding_from_bytes.close();
                    (samples, codec_params)
                } else if self.filepath.is_none() != true {
                    let trace_decoding_from_local_filepath = trace.create_child(String::from("Decoding from local filepath"));
                    let filepath = self.filepath.as_ref().unwrap();
                    let (samples, codec_params) = decoder::decode_from_local_filepath(
                        trace_decoding_from_local_filepath, filepath, self.file_start_time, limit_time_to_load
                    );
                    trace_decoding_from_local_filepath.close();
                    (samples, codec_params)
                } else if self.file_url.is_none() != true {
                    let trace_decoding_from_file_url = trace.create_child(String::from("Decoding from file url"));
                    let file_url = self.file_url.as_ref().unwrap();
                    let (samples, codec_params) = decoder::decode_from_file_url(
                        trace_decoding_from_file_url, file_url, self.file_start_time, limit_time_to_load
                    ).await;
                    trace_decoding_from_file_url.close();
                    (samples, codec_params)
                } else {
                    panic!("file_bytes, filepath or file_url must be specified");
                }
            },
            "speech" => {
                let synthesised_dialogue_response_result = engine_api_client::synthesise_get_dialogue(
                    engine_api_data, self.text.clone().unwrap(), self.voice_key.clone().unwrap()
                ).await;
                match synthesised_dialogue_response_result {
                    Ok(synthesised_dialogue_response) => {
                        match synthesised_dialogue_response {
                            Some(synthesised_dialogue_response_data) => {
                                let protocol = synthesised_dialogue_response_data.protocol.unwrap();
                                match protocol.as_str() {
                                    "url" => {
                                        let trace_decoding_from_file_url = trace.create_child(String::from("Decoding speech from file url"));
                                        let (samples, codec_params) = decoder::decode_from_file_url(
                                            trace_decoding_from_file_url, &*synthesised_dialogue_response_data.url.unwrap(), self.file_start_time, limit_time_to_load
                                        ).await;
                                        trace_decoding_from_file_url.close();
                                        (samples, codec_params)
                                    },
                                    "bytes" => {
                                        let trace_decoding_from_bytes = trace.create_child(String::from("Decoding speech from bytes"));
                                        let encoded_bytes = synthesised_dialogue_response_data.bytes.as_ref().unwrap();
                                        let boxed_file_bytes =  base64::decode(encoded_bytes).unwrap().into_boxed_slice();
                                        let (samples, codec_params) = decoder::decode_from_bytes(
                                            trace_decoding_from_bytes, boxed_file_bytes, String::from("mp3"), self.file_start_time, limit_time_to_load
                                        );
                                        // todo: make file extension dynamic
                                        trace_decoding_from_bytes.close();
                                        (samples, codec_params)
                                    }
                                    _ => { panic!("Protocol {} not supported", protocol) }
                                }
                            },
                            None => { panic!("Error in dialogue synthesis"); }
                        }
                    },
                    Err(_) => { panic!("Error in dialogue synthesis"); }
                }
            },
            _ => { panic!("Clip type {} not supported", self.clip_type); }
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
