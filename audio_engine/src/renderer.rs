use crate::models::{ReceivedParsedData, AudioBlock, Time};
use std::time::Instant;
use hound::{WavReader};
use std::io::BufReader;
use std::fs::File;
use std::num::Wrapping;
use std::borrow::{BorrowMut};
use crate::audio_clip::AudioClip;
use std::cell::{RefCell, RefMut, Ref};
use std::collections::HashMap;
use std::cmp::min;


struct RenderedClipInfos {
    player_start_time: i16,
    player_end_time: i16
}

pub struct Renderer {
    out_samples: Vec<i16>,
    target_spec: hound::WavSpec,
    rendered_clips_infos: HashMap<String, RenderedClipInfos>,
}


impl Renderer {
    pub async fn render(data: &ReceivedParsedData) -> Vec<i16> {
        let mut renderer = Renderer {
            out_samples: Vec::new(),
            target_spec: hound::WavSpec {
                channels: 1,
                sample_rate: data.target_spec.sample_rate as u32,
                bits_per_sample: 16,
                sample_format: hound::SampleFormat::Int,
            },
            rendered_clips_infos: HashMap::new()
        };
        renderer.render_to_vec(&data.blocks).await;
        renderer.out_samples
    }

    fn handle_track_start_time_relation(&self, time: &Time) -> i16 {
        time.offset.unwrap_or(0)
    }

    fn handle_audio_clip_start_time_relation(&self, time: &Time) -> i16 {
       if time.relationship_parent_id.is_none() {
            panic!("A relation was audio-clip_start-time but had no relationship_parent_id");
        } else {
            let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
            if self.rendered_clips_infos.contains_key(relationship_parent_id) {
                let relation_ship_clip_infos = self.rendered_clips_infos.get(relationship_parent_id).unwrap();
                relation_ship_clip_infos.player_start_time + time.offset.unwrap_or(0)
            } else {
                panic!("wrong order !");
                // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
            }
        }
    }

    fn handle_audio_clip_end_time_relation(&self, time: &Time) -> i16 {
       if time.relationship_parent_id.is_none() {
            panic!("A relation was audio-clip_end-time but had no relationship_parent_id");
        } else {
            let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
            if self.rendered_clips_infos.contains_key(relationship_parent_id) {
                let relation_ship_clip_infos = self.rendered_clips_infos.get(relationship_parent_id).unwrap();
                relation_ship_clip_infos.player_end_time + time.offset.unwrap_or(0)
            } else {
                panic!("wrong order !");
                // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
            }
        }
    }

    fn render_player_start_time(&mut self, audio_clip: &AudioClip) -> i16 {
        let type_key = &*audio_clip.player_start_time.type_key;
        match type_key {
            "track_start-time" => self.handle_track_start_time_relation(&audio_clip.player_start_time),
            "audio-clip_start-time" => self.handle_audio_clip_start_time_relation(&audio_clip.player_start_time),
            "audio-clip_end-time" => self.handle_audio_clip_end_time_relation(&audio_clip.player_start_time),
            _ => panic!("Unsupported type_key {}", type_key)
        }
    }

    fn render_player_start_time_to_sample_index(&mut self, audio_clip: &AudioClip) -> usize {
        self.render_player_start_time(audio_clip) as usize * self.target_spec.sample_rate as usize
    }

    fn render_player_end_time(&mut self, audio_clip: &AudioClip) -> Option<i16> {
        let type_key = &*audio_clip.player_end_time.type_key;
        match type_key {
            "until-self-end" => None,
            "track_start-time" => Some(self.handle_track_start_time_relation(&audio_clip.player_end_time)),
            "audio-clip_start-time" => Some(self.handle_audio_clip_start_time_relation(&audio_clip.player_end_time)),
            "audio-clip_end-time" => Some(self.handle_audio_clip_end_time_relation(&audio_clip.player_end_time)),
            _ => panic!("Unsupported type_key {}", type_key)
        }
    }

    fn render_player_end_time_to_sample_index(&mut self, audio_clip: &AudioClip) -> Option<usize> {
        if let Some(player_end_time) = self.render_player_end_time(audio_clip) {
            Some(player_end_time as usize * self.target_spec.sample_rate as usize)
        } else { None }
    }

    async fn render_to_vec(&mut self, audio_blocks: &Vec<AudioBlock>) {
        // todo: optimize the re-use of the multi file multiple times

        let start = Instant::now();
        if audio_blocks.len() > 0 {
            let mut first_audio_block = audio_blocks.get(0).unwrap();
            let borrowed_first_audio_block = first_audio_block.borrow_mut();
            let mut first_track = borrowed_first_audio_block.tracks.get(0).unwrap();
            let borrowed_first_track = first_track.borrow_mut();
            let audio_clips: &Vec<RefCell<AudioClip>> = &borrowed_first_track.clips;

            // todo: fix that and support multiple audio blocks instead of just using the first one

            let mut clips_pending_relationships_rendering: HashMap<String, Vec<&RefCell<AudioClip>>> = HashMap::new();

            for audio_clip_ref in audio_clips.iter() {
                let mut audio_clip = audio_clip_ref.borrow_mut();
                let cloned_clip_id = audio_clip.clip_id.clone();

                let player_start_time = self.render_player_start_time(&audio_clip);
                let player_end_time = self.render_player_end_time(&audio_clip);
                let limit_time_to_load: Option<i16> = if !player_end_time.is_none() {
                    let player_limit_time_to_load = player_end_time.unwrap() - player_start_time;
                    if audio_clip.file_end_time.is_none() {
                        Some(player_limit_time_to_load)
                    } else {
                        let file_limit_time_to_load = audio_clip.file_end_time.unwrap() - audio_clip.file_start_time;
                        Some(min(player_limit_time_to_load, file_limit_time_to_load))
                    }
                } else if !audio_clip.file_end_time.is_none() {
                    Some(audio_clip.file_end_time.unwrap() - audio_clip.file_start_time)
                } else { None };
                println!("limit_time_to_load: {:?}", limit_time_to_load);

                audio_clip.resample(self.target_spec, limit_time_to_load).await;
                let audio_clip_resamples = audio_clip.resamples.as_ref().unwrap();

                let render_clips_infos = RenderedClipInfos {
                    player_start_time,
                    player_end_time: player_end_time.unwrap_or(
                        player_start_time + ((audio_clip_resamples.len() / self.target_spec.sample_rate as usize) as i16)
                    )
                };
                self.render_clip(audio_clip_resamples, &render_clips_infos).await;
                self.rendered_clips_infos.insert(cloned_clip_id, render_clips_infos);

                // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
            }
        }
        // todo: handle audio clip being loaded before its relationship parent(s)
        println!("Total rendering time : {}ms", start.elapsed().as_millis());
    }

    async fn render_clip(&mut self, mut audio_clip_resamples: &Vec<i16>, render_clip_infos: &RenderedClipInfos) {
        // todo: file start time and file end time
        let outing_start = Instant::now();

        let player_start_sample_index = render_clip_infos.player_start_time as usize * self.target_spec.sample_rate as usize;
        let player_end_sample_index = render_clip_infos.player_end_time as usize * self.target_spec.sample_rate as usize;

        if player_end_sample_index > self.out_samples.len() {
            // We initialize all the required samples to zero here instead of checking in the below  sample assignation loop if we need to
            // create a new value or if we can just assign the  existing sample value in a new index. This will make the code go slower with
            // only a few clips, where we perform more initialization and unnecessary addition, but if we have tons of clips, the initialization
            // will be more rarely, and not doing any index comparison in the sample assignation loop will give us more performance. We prioritize
            // the fastest performance when we will have a ton of computation, rather than faster performance when we will have way less computation.
            let num_empty_samples_to_add = player_end_sample_index - (self.out_samples.len() - 1);
            for _ in 0..num_empty_samples_to_add {
                self.out_samples.push(0);
            }
        }
        let num_samples_to_write = player_end_sample_index - player_start_sample_index;
        let index_last_out_sample_to_write = player_start_sample_index + num_samples_to_write;
        let index_num_clip_samples = audio_clip_resamples.len() - 1;

        let mut input_index = 0;
        for i_output_sample in player_start_sample_index..index_last_out_sample_to_write {
            self.out_samples[i_output_sample] = (
                Wrapping(self.out_samples[i_output_sample]) +
                Wrapping(audio_clip_resamples[input_index])
            ).0;
            input_index += 1;
            if input_index >= index_num_clip_samples {
                input_index -= index_num_clip_samples;
                println!("Looping clip by resetting input index");
            }
        }
        println!("\nFinished outing.\n  --execution_time:{}ms", outing_start.elapsed().as_millis());
    }
}