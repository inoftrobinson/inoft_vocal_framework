use crate::models::{ReceivedParsedData, AudioBlock, Time, EngineApiData};
use std::num::Wrapping;
use std::borrow::{BorrowMut};
use crate::audio_clip::AudioClip;
use std::cell::{RefCell, RefMut};
use std::collections::HashMap;
use crate::tracer::TraceItem;
use std::cmp::{min};
use hound::WavSpec;
use audio_effects::audio_compressor::{AudioCompressor};
use audio_effects::base_transformer::BaseTransformer;
use audio_effects::tremolo::Tremolo;
// use rustfft::{FftPlanner, num_complex::Complex};
use ndarray::{Array, Axis, OwnedRepr, ArrayBase};
use ndarray_stats::QuantileExt;
// use rustfft::num_traits::ToPrimitive;
use realfft::RealFftPlanner;
use realfft::num_traits::real::Real;


pub struct RenderedClipInfos {
    // We use floats instead of ints, otherwise we could lose second precision, and cut/extend a file for too long.
    // Technically, we could store the player_sample_indexes instead of floats, but this would require to adjust
    // the sample from/to the target rate and the file's rate. Its simpler to keep track of the time, by using floats
    // to avoid losing precision. No heavy operations are performed on those floats, so they should not be too heavy.
    player_start_time: f32,
    player_end_time: f32
}

pub struct Renderer {
    out_samples: Vec<i16>,
    target_spec: hound::WavSpec,
    rendered_clips_infos: HashMap<String, RenderedClipInfos>,
}

struct PreAudioClipContainer<'a> {
    audio_clip_ref: &'a RefCell<AudioClip>,
    player_start_time: f32,
    player_end_time: Option<f32>
}

struct PreAudioClipsContainer<'a> {
    audio_clips_containers: Vec<PreAudioClipContainer<'a>>,
    smallest_player_start_time: f32,
    biggest_player_end_time: Option<f32>
}


impl Renderer {
    pub async fn render(trace: &mut TraceItem, data: &ReceivedParsedData) -> Vec<i16> {
        let target_wav_spec = data.target_spec.to_wav_spec();
        let mut renderer = Renderer {
            out_samples: Vec::new(),
            target_spec: target_wav_spec,
            rendered_clips_infos: HashMap::new(),
        };
        renderer.render_to_vec(trace, &data.engine_api_data, &data.blocks).await;
        renderer.out_samples
    }

    fn handle_track_start_time_relation(&self, time: &Time) -> f32 {
        time.offset.unwrap_or(0.0)
    }

    fn handle_audio_clip_start_time_relation(&self, time: &Time) -> f32 {
       if time.relationship_parent_id.is_none() {
            panic!("A relation was audio-clip_start-time but had no relationship_parent_id");
       } else {
           let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
           if self.rendered_clips_infos.contains_key(relationship_parent_id) {
               let relation_ship_clip_infos = self.rendered_clips_infos.get(relationship_parent_id).unwrap();
               relation_ship_clip_infos.player_start_time + time.offset.unwrap_or(0.0)
           } else {
               panic!("wrong order !");
               // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
           }
       }
    }

    fn handle_audio_clip_end_time_relation(&self, time: &Time) -> f32 {
       if time.relationship_parent_id.is_none() {
            panic!("A relation was audio-clip_end-time but had no relationship_parent_id");
        } else {
            let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
            if self.rendered_clips_infos.contains_key(relationship_parent_id) {
                let relation_ship_clip_infos = self.rendered_clips_infos.get(relationship_parent_id).unwrap();
                relation_ship_clip_infos.player_end_time + time.offset.unwrap_or(0.0)
            } else {
                panic!("wrong order !");
                // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
            }
        }
    }

    fn handle_until_self_end_relation(&self, time: &Time) -> f32 {
        panic!("Not yet implemented");
        if time.relationship_parent_id.is_none() {
            panic!("A relation was audio-clip_end-time but had no relationship_parent_id");
        } else {
            let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
            if self.rendered_clips_infos.contains_key(relationship_parent_id) {
                let relation_ship_clip_infos = self.rendered_clips_infos.get(relationship_parent_id).unwrap();
                relation_ship_clip_infos.player_end_time + time.offset.unwrap_or(0.0)
            } else {
                panic!("wrong order !");
                // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
            }
        }
    }

    fn render_player_start_time(&mut self, audio_clip: &AudioClip) -> f32 {
        let type_key = &*audio_clip.player_start_time.type_key;
        // until-self-end should not be acceptable and generable by the Python audio editing
        match type_key {
            "until-self-end" => self.handle_audio_clip_end_time_relation(&audio_clip.player_start_time),
            "track_start-time" => self.handle_track_start_time_relation(&audio_clip.player_start_time),
            "audio-clip_start-time" => self.handle_audio_clip_start_time_relation(&audio_clip.player_start_time),
            "audio-clip_end-time" => self.handle_audio_clip_end_time_relation(&audio_clip.player_start_time),
            _ => panic!("Unsupported type_key {}", type_key)
        }
    }

    fn render_player_start_time_to_sample_index(&mut self, audio_clip: &AudioClip) -> usize {
        (self.render_player_start_time(audio_clip) * self.target_spec.sample_rate as f32) as usize
    }

    fn render_player_end_time(&mut self, audio_clip: &AudioClip) -> Option<f32> {
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
            Some((player_end_time * self.target_spec.sample_rate as f32) as usize)
        } else { None }
    }

    async fn render_to_vec(&mut self, trace: &mut TraceItem, engine_api_data: &EngineApiData, audio_blocks: &Vec<AudioBlock>) {
        // todo: optimize the re-use of the multi file multiple times
        if audio_blocks.len() > 0 {
            // todo: fix that and support multiple audio blocks instead of just using the first one
            let mut first_audio_block = audio_blocks.get(0).unwrap();
            let borrowed_first_audio_block = first_audio_block.borrow_mut();
            for mut track_ref in borrowed_first_audio_block.tracks.iter() {
                let borrowed_current_track = track_ref.borrow_mut();
                let track_audio_clips: &Vec<RefCell<AudioClip>> = &borrowed_current_track.clips;

                for audio_clip_ref in track_audio_clips.iter() {
                    let mut audio_clip = audio_clip_ref.borrow_mut();
                    let trace_clip = trace.create_child(String::from(format!("clip_{}", audio_clip.clip_id)));
                    let cloned_clip_id = audio_clip.clip_id.clone();

                    let trace_player_times_rendering = trace_clip.create_child(String::from("player_times_rendering"));
                    let player_start_time = self.render_player_start_time(&audio_clip);
                    let player_end_time = self.render_player_end_time(&audio_clip);
                    let limit_time_to_load: Option<f32> = if !player_end_time.is_none() {
                        let player_limit_time_to_load = player_end_time.unwrap() - player_start_time;
                        if audio_clip.file_end_time.is_none() {
                            Some(player_limit_time_to_load)
                        } else {
                            let file_limit_time_to_load = audio_clip.file_end_time.unwrap() - audio_clip.file_start_time;
                            Some(file_limit_time_to_load.min(player_limit_time_to_load))
                        }
                    } else if !audio_clip.file_end_time.is_none() {
                        Some(audio_clip.file_end_time.unwrap() - audio_clip.file_start_time)
                    } else { None };
                    println!("limit_time_to_load: {:?}", limit_time_to_load);
                    trace_player_times_rendering.close();

                    let trace_resampling = trace_clip.create_child(String::from("resampling"));
                    audio_clip.resample(trace_resampling, engine_api_data, self.target_spec, limit_time_to_load).await;
                    let audio_clip_resamples = audio_clip.resamples.as_ref().unwrap();
                    trace_resampling.close();

                    let trace_clip_rendering = trace_clip.create_child(String::from("rendering"));
                    let render_clips_infos = RenderedClipInfos {
                        player_start_time,
                        player_end_time: player_end_time.unwrap_or(
                            player_start_time + (audio_clip_resamples.len() as f32 / self.target_spec.sample_rate as f32)
                        )
                    };

                    let clip_final_volume = audio_clip.volume.unwrap().clone();
                    // todo: take in consideration the track volume to compute the clip final volume

                    self.render_clip(
                        trace_clip_rendering, clip_final_volume, audio_clip_resamples,
                        &audio_clip.effects, &render_clips_infos
                    ).await;
                    self.rendered_clips_infos.insert(cloned_clip_id, render_clips_infos);
                    // clips_pending_relationships_rendering.entry(relationship_parent_id.clone()).or_insert(Vec::new()).push(audio_clip_ref);
                    trace_clip_rendering.close();
                    println!("\nFinished render clip.\n  --execution_time:{}ms", trace_clip_rendering.elapsed);

                    trace_clip.close();
                }

                let mut clips_pending_relationships_rendering: HashMap<String, Vec<&RefCell<AudioClip>>> = HashMap::new();

                /*let mut clips_by_file_urls: HashMap<String, Vec<&RefCell<AudioClip>>> = HashMap::new();
                let mut clips_by_file_paths: HashMap<String, PreAudioClipsContainer> = HashMap::new();

                for audio_clip_ref in audio_clips.iter() {
                    let audio_clip = audio_clip_ref.borrow();
                    if !audio_clip.file_url.is_none() {
                        let file_url = audio_clip.file_url.as_ref().unwrap();
                        // clips_by_file_urls.entry(file_url.clone()).or_insert(Vec::new()).push(audio_clip_ref);
                    } else if !audio_clip.filepath.is_none() {
                        let player_start_time = self.render_player_start_time(&audio_clip);
                        let player_end_time = self.render_player_end_time(&audio_clip);
                        let audio_clip_container = PreAudioClipContainer { audio_clip_ref, player_start_time, player_end_time };

                        let filepath = audio_clip.filepath.as_ref().unwrap();
                        if clips_by_file_paths.contains_key(filepath) {
                            let mut container = clips_by_file_paths.get_mut(filepath).unwrap();
                            container.audio_clips_containers.push(audio_clip_container);
                            if player_start_time < container.smallest_player_start_time {
                                container.smallest_player_start_time = player_start_time
                            }
                            if !container.biggest_player_end_time.is_none() {
                                if player_end_time.is_none() || player_end_time.unwrap() > container.biggest_player_end_time.unwrap() {
                                    container.biggest_player_end_time = player_end_time;
                                }
                            }
                        }
                        // clips_by_file_paths.entry(audio_clip.filepath.unwrap().clone()).or_insert(Vec::new()).push(audio_clip_ref);
                    }
                }
                for container in clips_by_file_paths.values() {
                    println!("biggest_player_end_time {:?}", container.biggest_player_end_time);
                    println!("smallest_player_start_time {}", container.smallest_player_start_time);
                }
                 */
            }
        }


        // todo: allow to apply effects on tracks or the entire project
        /*let mut transformers: Vec<Box<dyn BaseTransformer>> = vec![
            // Box::new(AudioCompressor::new(&self.target_spec))
            Box::new(Tremolo::new(&self.target_spec))
        ];

        if transformers.len() > 0 {
            for i_sample in 0..self.out_samples.len() {
                let mut sample_value = self.out_samples[i_sample];
                for i_transformer in 0..transformers.len() {
                    sample_value = transformers[i_transformer].alter_sample(sample_value, i_sample);
                }
                self.out_samples[i_sample] = sample_value;
            }
        }*/

        // todo: handle audio clip being loaded before its relationship parent(s)
        trace.close();
        // trace.to_file("F:/Inoft/anvers_1944_project/inoft_vocal_framework/dist/json/trace.json");
    }

    async fn render_clip(
        &mut self, trace: &mut TraceItem, volume: u16, audio_clip_resamples: &Vec<i16>,
        effects_ref: &RefCell<Vec<Box<dyn BaseTransformer<i16>>>>, render_clip_infos: &RenderedClipInfos
    ) {
        // todo: file start time and file end time

        let trace_initialization = trace.create_child(String::from("Initialization"));
        let player_start_sample_index = (render_clip_infos.player_start_time * self.target_spec.sample_rate as f32) as usize;
        let player_end_sample_index = (render_clip_infos.player_end_time * self.target_spec.sample_rate as f32) as usize;
        let num_samples_to_write = player_end_sample_index - player_start_sample_index;
        let index_last_out_sample_to_write = player_start_sample_index + num_samples_to_write;
        let index_num_clip_samples = audio_clip_resamples.len() - 1;
        trace_initialization.close();

        let trace_populating_with_empty_samples = trace.create_child(String::from("Populating with empty samples"));
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
        trace_populating_with_empty_samples.close();

        let volume_multiplicative = volume as f32 / 100.0;

        let trace_writing_samples = trace.create_child(String::from("Writing samples"));
        let mut input_index = 0;
        for i_output_sample in player_start_sample_index..index_last_out_sample_to_write {
            let mut current_sample_value = (audio_clip_resamples[input_index] as f32 * volume_multiplicative) as i16;
            let mut effects_items = effects_ref.borrow_mut();
            for i_effect in 0..effects_items.len() {
                current_sample_value = effects_items[i_effect].alter_sample(current_sample_value, i_output_sample);
            }

            let mut combined_sample_value = ((
                Wrapping(self.out_samples[i_output_sample]) +
                Wrapping(current_sample_value)
            ).0);
            self.out_samples[i_output_sample] = combined_sample_value;
            input_index += 1;
            if input_index >= index_num_clip_samples {
                input_index -= index_num_clip_samples;
                println!("Looping clip by resetting input index");
            }
        }
        trace_writing_samples.close();
    }
}