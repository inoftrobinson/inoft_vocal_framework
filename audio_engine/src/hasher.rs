use crate::models::{ReceivedParsedData, Time, AudioClip, Track};
use std::time::Instant;
use sha2::{Sha512, Digest};
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use std::cell::{Ref, RefCell};
use std::borrow::Borrow;


#[derive(Serialize, Deserialize)]
pub struct ClipWithHashedChildren {
    filepath: Option<String>,
    file_url: Option<String>,
    volume: Option<u16>,
    player_start_time: Time,
    player_end_time: Time,
    file_start_time: f32,
    file_end_time: Option<f32>,
}

#[derive(Serialize, Deserialize)]
pub struct TrackInfos {
    gain: i16,
}

pub struct AudioBlockContainer {
    tracks: Vec<TrackContainer>,
}

pub struct TrackContainer {
    track_id: String,
    clips: Vec<ClipContainer>,
}

pub struct ClipContainer {
    clip_id: String,
    parent_track_id: String,
}

#[derive(Serialize, Deserialize)]
pub struct TrackWithHashedChildren {
    gain: i16,
    clips_signature: String,
}

#[derive(Serialize, Deserialize)]
pub struct AudioBlockWithHashedChildren {
    tracks_signature: String,
}

#[derive(Serialize, Deserialize)]
pub struct AudioProjectWithHashedChildren {
    sample_rate: u32,
    audio_blocks_signature: String,
}


pub struct Hasher {
    sha_hasher: Sha512,
    clips_waiting_by_parent_id: HashMap<Vec<String>, Vec<&'static RefCell<AudioClip>>>,
    elements_ids_to_signatures: HashMap<String, String>,
    clips_signatures: Vec<String>,
    tracks_signatures: Vec<String>,
}

impl Hasher {
    pub fn hash(data: &ReceivedParsedData) -> String {
        let start = Instant::now();
        let signature = Hasher {
            sha_hasher: Sha512::new(),
            clips_waiting_by_parent_id: HashMap::new(),
            elements_ids_to_signatures: HashMap::new(),
            clips_signatures: Vec::new(),
            tracks_signatures: Vec::new()
        }.execute_hash(data);
        println!("\nFinished hashing.\n  --execution_time:{}ms", (start.elapsed().as_micros() as f64 / 1000.0));
        signature
    }

    fn find_parent_of_relationship(&self, relationship_parent_id: Option<String>) {

    }

    /*fn register_relationship(&mut self, relationship_parent_id: &Option<String>) {
       if !relationship_parent_id.is_none() {
            required_parents.push(relationship_parent_id.unwrap());
        }
    }*/

    fn render_time(&self, time: &Time) -> Time {
        if !time.relationship_parent_id.is_none() {
            let mut altered_time = time.clone();
            let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
            let matching_signature = self.elements_ids_to_signatures.get(&*relationship_parent_id);
            altered_time.relationship_parent_id = Some(matching_signature.expect(
                &*format!("Signature not found for element {}", relationship_parent_id)
            ).clone());
            altered_time
        } else {
            time.clone()  // todo: is clone necessary here ?
        }
    }

    fn sign_clip(&mut self, clip: Ref<AudioClip>) {
        /*self.register_relationship(&clip.player_start_time.relationship_parent_id);
        self.register_relationship(&clip.player_end_time.relationship_parent_id);*/

        let clip_with_hashed_children = serde_json::to_string(
            &ClipWithHashedChildren {
                filepath: clip.filepath.clone(),
                file_url: clip.file_url.clone(),
                volume: clip.volume,
                player_start_time: self.render_time(&clip.player_start_time),
                player_end_time: self.render_time(&clip.player_end_time),
                file_start_time: clip.file_start_time,
                file_end_time: clip.file_end_time
            }
        ).unwrap();
        self.sha_hasher.update(clip_with_hashed_children);
        let clip_signature = format!("{:X}", self.sha_hasher.finalize_reset());
        self.elements_ids_to_signatures.insert(clip.clip_id.clone(), clip_signature.clone());
        self.clips_signatures.push(clip_signature);
    }

    fn sign_track(&mut self, track: &Track) {
        let track_infos = serde_json::to_string(
            &TrackInfos {
                gain: track.gain,
            }
        ).unwrap();
        self.sha_hasher.update(track_infos);
        let track_signature = format!("{:X}", self.sha_hasher.finalize_reset());
        self.elements_ids_to_signatures.insert(track.track_id.clone(), track_signature.clone());
        self.tracks_signatures.push(track_signature);
    }
    
    fn execute_hash(&mut self, data: &ReceivedParsedData) -> String {
        let mut audio_blocks_containers: Vec<AudioBlockContainer> = Vec::new();
        let mut audio_blocks_signatures: Vec<String> = Vec::new();

        for i_block in 0..data.blocks.len() {
            let mut audio_block_container = AudioBlockContainer { tracks: Vec::new() };
            let audio_block = &data.blocks[i_block];

            for track in audio_block.tracks.iter() {
                self.sign_track(track);
                let track_id = track.track_id.clone();
                let mut track_container = TrackContainer { track_id: track_id.clone(), clips: Vec::new() };

                for clip_ref in &track.clips {
                    let clip = clip_ref.borrow();
                    track_container.clips.push(ClipContainer { clip_id: clip.clip_id.clone(), parent_track_id: track_id.clone() });

                    let mut required_parents: Vec<String> = Vec::new();
                    if !clip.player_start_time.relationship_parent_id.is_none() {
                        required_parents.push(clip.player_start_time.relationship_parent_id.clone().unwrap());
                    }
                    if !clip.player_end_time.relationship_parent_id.is_none() {
                        required_parents.push(clip.player_end_time.relationship_parent_id.clone().unwrap());
                    }
                    if required_parents.len() > 0 {
                        // self.clips_waiting_by_parent_id.entry(required_parents).or_insert(Vec::new()).push(clip_ref);
                    } else {
                        self.sign_clip(clip);
                    }
                }
                audio_block_container.tracks.push(track_container);
            }
        }

        for (required_parent_ids, mut waiting_clips) in self.clips_waiting_by_parent_id.clone().into_iter() {
            let mut contains_alls = true;
            for parent_id in required_parent_ids.iter() {
                if self.elements_ids_to_signatures.contains_key(parent_id) {
                    contains_alls = false;
                    break;
                }
            }
            if contains_alls == true {
                for clip in waiting_clips.iter() {
                    let b: &RefCell<AudioClip> = clip.borrow();
                    let c: Ref<AudioClip> = b.borrow();
                    self.sign_clip(c);
                }
            }
        }

        for audio_block_container in audio_blocks_containers.iter() {
            let mut tracks_signatures: Vec<String> = Vec::new();  // todo: make fixed length
            for track_container in audio_block_container.tracks.iter() {
                /*let mut clips_signatures: Vec<String> = track_container.clips.iter().map(|item| {
                    let clip_id = &item.clip_ref.borrow().clip_id;
                    self.elements_ids_to_signatures.get(clip_id).expect(&*format!("Signature not found for clip {}", clip_id))
                }).collect();*/
                let mut clips_signatures: Vec<String> = track_container.clips.iter().map(|item|
                    self.elements_ids_to_signatures.get(&item.clip_id.clone())
                        .expect(&*format!("Signature not found for clip {}", &item.clip_id))
                        .clone()
                ).collect::<Vec<String>>();
                clips_signatures.sort();  // Sort the clips signatures by alphabetical order

                let all_sorted_clips_signature = join_signatures(clips_signatures);
                let track_with_hashed_children = serde_json::to_string(
                    &TrackWithHashedChildren {
                        gain: 0,  // track_container.track.borrow().gain, todo: re-implement retrieval of gain
                        clips_signature: all_sorted_clips_signature
                    }
                ).unwrap();
                self.sha_hasher.update(track_with_hashed_children);
                tracks_signatures.push(format!("{:X}", self.sha_hasher.finalize_reset()));
            }
            tracks_signatures.sort();  // Sort the tracks signatures by alphabetical order
            let all_sorted_tracks_signature = join_signatures(tracks_signatures);

            let audio_block_with_hashed_children = serde_json::to_string(
                &AudioBlockWithHashedChildren {
                    tracks_signature: all_sorted_tracks_signature
                }
            ).unwrap();
            self.sha_hasher.update(audio_block_with_hashed_children);
            audio_blocks_signatures.push(format!("{:X}", self.sha_hasher.finalize_reset()));
        }
        audio_blocks_signatures.sort();  // Sort the audio blocks signatures by alphabetical order
        let all_sorted_audio_blocks_signature = join_signatures(audio_blocks_signatures);
    
        let audio_project_with_hashed_children = serde_json::to_string(
            &AudioProjectWithHashedChildren {
                sample_rate: data.target_spec.sample_rate,
                audio_blocks_signature: all_sorted_audio_blocks_signature
            }
        ).unwrap();
        // Everything that needed sorting has already been sorted at this point
        self.sha_hasher.update(audio_project_with_hashed_children);
        let audio_project_signature = format!("{:X}", self.sha_hasher.finalize_reset());
    
        audio_project_signature
    }
}

fn join_signatures(signatures: Vec<String>) -> String {
    signatures.join("-")
}
