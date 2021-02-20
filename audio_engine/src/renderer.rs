use crate::models::{ReceivedParsedData, AudioBlock};
use std::time::Instant;
use hound::{WavReader};
use std::io::BufReader;
use std::fs::File;
use std::num::Wrapping;
use std::borrow::{BorrowMut};
use crate::audio_clip::AudioClip;
use std::cell::{RefCell, RefMut, Ref};
use std::collections::HashMap;


struct RenderedClipInfos {
    player_start_sample_index: usize,
    player_end_sample_index: usize
}

pub struct Renderer {
    out_samples: Vec<i16>,
    target_spec: hound::WavSpec
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
            }
        };
        renderer.render_to_vec(&data.blocks).await;
        renderer.out_samples
    }

    async fn render_to_vec(&mut self, audio_blocks: &Vec<AudioBlock>) {
        let start = Instant::now();
        if audio_blocks.len() > 0 {
            let mut first_audio_block = audio_blocks.get(0).unwrap();
            let borrowed_first_audio_block = first_audio_block.borrow_mut();
            let mut first_track = borrowed_first_audio_block.tracks.get(0).unwrap();
            let borrowed_first_track = first_track.borrow_mut();
            let audio_clips: &Vec<RefCell<AudioClip>> = &borrowed_first_track.clips;

            // todo: fix that and support multiple audio blocks instead of just using the first one

            let mut rendered_clips_infos: HashMap<String, RenderedClipInfos> = HashMap::new();
            let mut clips_pending_relationships_rendering: HashMap<String, Vec<&RefCell<AudioClip>>> = HashMap::new();

            for audio_clip_ref in audio_clips.iter() {
                let mut audio_clip = audio_clip_ref.borrow_mut();

                let type_key = &*audio_clip.player_start_time.type_key;
                match type_key {
                    "track_start-time" => {
                        let start_time = audio_clip.player_start_time.offset.unwrap_or(0);
                        rendered_clips_infos.insert(audio_clip.clip_id.clone(), self.render_clip(audio_clip, start_time).await);
                    },
                    "audio-clip_start-time" => {
                        if audio_clip.player_start_time.relationship_parent_id.is_none() {
                            println!("An audio clip was audio-clip_start-time but had no relationship_parent_id");
                            rendered_clips_infos.insert(audio_clip.clip_id.clone(), self.render_clip(audio_clip, 0).await);
                        } else {
                            let relationship_parent_id = audio_clip.player_start_time.relationship_parent_id.as_ref().unwrap();
                            if rendered_clips_infos.contains_key(relationship_parent_id) {
                                let parent_player_start_time = rendered_clips_infos.get(relationship_parent_id).unwrap().player_start_sample_index / self.target_spec.sample_rate as usize;
                                // todo: move the sample index instead of doing a division here to correct
                                let start_time = parent_player_start_time as i16 + audio_clip.player_start_time.offset.unwrap();
                                rendered_clips_infos.insert(audio_clip.clip_id.clone(), self.render_clip(audio_clip, start_time).await);
                            } else {
                                clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
                            }
                        }
                    }
                    _ => panic!("Unsupported type_key {}", type_key)
                };
            }
        }
        // todo: handle audio clip being loaded before its relationship parent(s)
        println!("Total rendering time : {}ms", start.elapsed().as_millis());
    }

    async fn render_clip(&mut self, mut audio_clip: RefMut<'_, AudioClip>, seconds_start_time: i16) -> RenderedClipInfos {
        audio_clip.resample(self.target_spec).await;
        let audio_clip_resamples = audio_clip.resamples.as_ref().unwrap();

        println!("seconds_start_time : {}", seconds_start_time);
        println!("sample_rate : {}", self.target_spec.sample_rate);
        let player_start_sample_index = seconds_start_time as usize * self.target_spec.sample_rate as usize;
        println!("player_start_sample_index : {}", player_start_sample_index);
        let player_end_sample_index = player_start_sample_index + audio_clip_resamples.len();

        // todo: file start time and file end time

        let outing_start = Instant::now();
        println!("start_time: {:?}", audio_clip.player_start_time.offset);
        // let player_start_sample = audio_clip.render_player_start_time_to_sample_index(target_spec.sample_rate);
        // let end_sample = audio_clip.render_player_end_time_to_sample_index(target_spec.sample_rate);

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
        for i_sample in 0..audio_clip_resamples.len() {
            let current_sample_index = i_sample + player_start_sample_index;
            self.out_samples[current_sample_index] = (
                Wrapping(self.out_samples[current_sample_index]) +
                Wrapping(audio_clip_resamples[i_sample])
            ).0;
        }

        println!("\nFinished outing.\n  --execution_time:{}ms", outing_start.elapsed().as_millis());
        RenderedClipInfos { player_start_sample_index, player_end_sample_index }
    }
}