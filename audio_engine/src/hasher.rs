use crate::models::{ReceivedParsedData, Time, AudioClip, Track, AudioBlock};
use std::time::Instant;
use sha2::{Sha512, Digest};
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use std::cell::{Ref, RefCell};
use std::borrow::Borrow;
use std::ops::Deref;


#[derive(Serialize, Deserialize)]
pub struct TrackInfos {
    gain: i16,
}

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

pub struct TrackContainer<'a> {
    track: &'a Track,
    clips: Vec<ClipContainer>,
}

pub struct ClipContainer {
    clip_id: String,
    parent_track_id: String,
}

pub struct ClipRenderContainer<'a> {
    clip: &'a RefCell<AudioClip>,
    requirements_ids: Vec<String>,
}


pub struct AudioBlockHasher<'a> {
    sha_hasher: &'a mut Sha512,
    clips_waiting_by_individual_parent_id: HashMap<String, Vec<ClipRenderContainer<'a>>>,
    elements_ids_to_signatures: HashMap<String, String>,
}

impl<'a> AudioBlockHasher<'a> {
    pub fn hash(audio_block: &'a AudioBlock, sha_hasher: &mut Sha512) -> String {
        AudioBlockHasher {
            sha_hasher,
            clips_waiting_by_individual_parent_id: HashMap::new(),
            elements_ids_to_signatures: HashMap::new(),
        }.execute_hash(audio_block)
    }

    fn sha_hash(&mut self, value: String) -> String {
        self.sha_hasher.update(value);
        format!("{:X}", self.sha_hasher.finalize_reset())
    }

    /*fn is_exempted(type_key: &str) -> bool {
        match type_key {
            "until-self-end" => true,
            "track_start-time" => false,
            "audio-clip_start-time" => false,
            "audio-clip_end-time" => false,
            _ => panic!("Unsupported type_key {}", type_key)
        }
    }*/

    fn is_time_relationship_parent_ready(&self, time: &Time) -> bool {
        // let is_exempted = AudioBlockHasher::is_exempted(&*time.type_key);
        // if !is_exempted && !time.relationship_parent_id.is_none() {
        if !time.relationship_parent_id.is_none() {
            let relationship_parent_id = time.relationship_parent_id.as_ref().unwrap();
            let matching_signature = self.elements_ids_to_signatures.get(&*relationship_parent_id);
            println!("matching_signature : {:?}", matching_signature);
            !matching_signature.is_none()
        } else {
            true
        }
    }

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
        let clip_signature = self.sha_hash(clip_with_hashed_children);
        self.elements_ids_to_signatures.insert(clip.clip_id.clone(), clip_signature.clone());
    }

    fn sign_track(&mut self, track: &Track) {
        let track_infos = serde_json::to_string(
            &TrackInfos {
                gain: track.gain,
            }
        ).unwrap();
        let track_signature = self.sha_hash(track_infos);
        self.elements_ids_to_signatures.insert(track.track_id.clone(), track_signature.clone());
    }

    fn rar(&mut self, clip_id: String) {
        let mut ready_clips: Vec<&RefCell<AudioClip>> = Vec::new();
        match self.clips_waiting_by_individual_parent_id.get_mut(&*clip_id) {
            Some(mut clips) => {
                for waiting_clip in clips.iter_mut() {
                    let mut contains_all_requirements = true;
                    for requirement_id in waiting_clip.requirements_ids.iter() {
                        if !self.elements_ids_to_signatures.contains_key(requirement_id) {
                            contains_all_requirements = false;
                            break;
                        }
                    }
                    if contains_all_requirements == true {
                        ready_clips.push(waiting_clip.clip);
                    }
                }
            },
            None => {}
        }
        // We render the clip outside of the clips_waiting loop, because clips_waiting_by_individual_parent_id
        // is assigned to the instance of the class,if would cause a compile error if tried to call the rar
        // function inside of the loop that is already borrowing self as immutable.
        for ready_clip in ready_clips.into_iter() {
            let borrowed = ready_clip.borrow();
            let clip_id = borrowed.clip_id.clone();
            self.sign_clip(borrowed);
            self.rar(clip_id);
        }
    }
    
    fn execute_hash(&mut self, audio_block: &'a AudioBlock) -> String {
        for track in audio_block.tracks.iter() {
            // We sign all tracks before starting the rendering of the relations, because the  'root clips' that
            // can be and need to be considered ready right away in order for their dependant clips to function,
            // will have relations that based themselves on the tracks. Either their parent track, or any other track.
            self.sign_track(track);
        }
        let mut tracks_containers: Vec<TrackContainer> = Vec::new();
        let mut root_clips_ids: Vec<String> = Vec::new();
        let mut clips_waiting_by_grouped_parents_ids: HashMap<Vec<String>, Vec<&RefCell<AudioClip>>> = HashMap::new();

        for track in audio_block.tracks.iter() {
            let track_id = track.track_id.clone();
            let mut track_container = TrackContainer { track, clips: Vec::new() };

            for i_clip in 0..track.clips.len() {
                let clip_ref = &track.clips[i_clip];
                let clip = clip_ref.borrow();
                track_container.clips.push(ClipContainer { clip_id: clip.clip_id.clone(), parent_track_id: track_id.clone() });

                let mut required_parents: Vec<String> = Vec::new();
                if !self.is_time_relationship_parent_ready(&clip.player_start_time) {
                    required_parents.push(clip.player_start_time.relationship_parent_id.clone().unwrap());
                }
                if !self.is_time_relationship_parent_ready(&clip.player_end_time) {
                    required_parents.push(clip.player_end_time.relationship_parent_id.clone().unwrap());
                }
                if required_parents.len() > 0 {
                    clips_waiting_by_grouped_parents_ids.entry(required_parents.clone()).or_insert(Vec::new()).push(clip_ref);
                    for parent in required_parents.iter() {
                        self.clips_waiting_by_individual_parent_id.entry(parent.clone()).or_insert(Vec::new())
                            .push(ClipRenderContainer { clip: &clip_ref, requirements_ids: required_parents.clone() });
                    }
                } else {
                    let clip_id = clip.clip_id.clone();
                    self.sign_clip(clip);
                    root_clips_ids.push(clip_id);
                }
            }
            tracks_containers.push(track_container);
        }

        if !(root_clips_ids.len() > 0) {
            panic!("Seems like you have no root clip :'(");
        }
        for root_clip_id in root_clips_ids {
            self.rar(root_clip_id);
        }

        let mut tracks_signatures: Vec<String> = Vec::new();  // todo: make fixed length
        for track_container in tracks_containers.iter() {
            let mut clips_signatures: Vec<String> = track_container.clips.iter()
                .map(|item| self.elements_ids_to_signatures
                    .get(&item.clip_id.clone())
                    .expect(&*format!("Signature not found for clip {}", &item.clip_id))
                    .clone()
                ).collect::<Vec<String>>();
            clips_signatures.sort();  // Sort the clips signatures by alphabetical order

            let all_sorted_clips_signature = join_signatures(clips_signatures);
            println!("joined : {}", all_sorted_clips_signature);
            let track_with_hashed_children = serde_json::to_string(
                &TrackWithHashedChildren {
                    gain: track_container.track.gain,
                    clips_signature: all_sorted_clips_signature
                }
            ).unwrap();
            tracks_signatures.push(self.sha_hash(track_with_hashed_children));
        }
        tracks_signatures.sort();  // Sort the tracks signatures by alphabetical order
        let all_sorted_tracks_signature = join_signatures(tracks_signatures);

        let audio_block_with_hashed_children = serde_json::to_string(
            &AudioBlockWithHashedChildren {
                tracks_signature: all_sorted_tracks_signature
            }
        ).unwrap();
        let audio_block_signature = self.sha_hash(audio_block_with_hashed_children);
        audio_block_signature
    }
}


pub struct AudioProjectHasher<'a> {
    sha_hasher: &'a mut Sha512,
}

impl<'a> AudioProjectHasher<'a> {
    pub fn hash(data: &'a ReceivedParsedData) -> String {
        let start = Instant::now();
        let signature = AudioProjectHasher {
            sha_hasher: &mut Sha512::new(),
        }.execute_hash(data);
        println!("\nFinished hashing.\n  --execution_time:{}ms", (start.elapsed().as_micros() as f64 / 1000.0));
        signature
    }

    fn sha_hash(&mut self, value: String) -> String {
        self.sha_hasher.update(value);
        format!("{:X}", self.sha_hasher.finalize_reset())
    }

    fn execute_hash(&mut self, data: &'a ReceivedParsedData) -> String {
        let mut audio_blocks_signatures: Vec<String> = data.blocks.iter()
            .map(|audio_block| AudioBlockHasher::hash(audio_block, self.sha_hasher))
            .collect();
        audio_blocks_signatures.sort();  // Sort the audio blocks signatures by alphabetical order
        let all_sorted_audio_blocks_signature = join_signatures(audio_blocks_signatures);

        let audio_project_with_hashed_children = serde_json::to_string(
            &AudioProjectWithHashedChildren {
                sample_rate: data.target_spec.sample_rate,
                audio_blocks_signature: all_sorted_audio_blocks_signature
            }
        ).unwrap();

        // Everything that needed sorting has already been sorted at this point
        let audio_project_signature = self.sha_hash(audio_project_with_hashed_children);
        audio_project_signature
    }
}


fn join_signatures(signatures: Vec<String>) -> String {
    signatures.join("-")
}
