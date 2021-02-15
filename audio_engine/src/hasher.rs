use crate::models::{ReceivedParsedData, Time};
use std::time::Instant;
use sha2::{Sha512, Digest};
use serde::{Serialize, Deserialize};


#[derive(Serialize, Deserialize)]
pub struct ClipWithHashedChildren {
    filepath: Option<String>,
    file_url: Option<String>,
    volume: Option<u8>,
    player_start_time: Time,
    player_end_time: Time,
    file_start_time: i16,
    file_end_time: i16,
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
    sample_rate: i32,
    audio_blocks_signature: String,
}


pub fn hash(data: &ReceivedParsedData) -> String {
    let start = Instant::now();
    let mut hasher = Sha512::new();

    let mut audio_blocks_signatures: Vec<String> = Vec::new();
    for i_block in 0..data.blocks.len() {
        let audio_block = &data.blocks[i_block];

        let mut tracks_signatures: Vec<String> = Vec::new();
        for track in &audio_block.tracks {
            let mut clips_signatures: Vec<String> = Vec::new();
            for clip_ref in &track.clips {
                let clip = clip_ref.borrow();
                let clip_with_hashed_children = serde_json::to_string(
                    &ClipWithHashedChildren {
                        filepath: clip.filepath.clone(),
                        file_url: clip.file_url.clone(),
                        volume: clip.volume,
                        player_start_time: clip.player_start_time.clone(),
                        player_end_time: clip.player_end_time.clone(),
                        file_start_time: clip.file_start_time,
                        file_end_time: clip.file_end_time
                    }
                ).unwrap();
                hasher.update(clip_with_hashed_children);
                clips_signatures.push(format!("{:X}", hasher.finalize_reset()));
            }
            clips_signatures.sort();  // Sort the clips signatures by alphabetical order
            let all_sorted_clips_signature = join_signatures(clips_signatures);

            let track_with_hashed_children = serde_json::to_string(
                &TrackWithHashedChildren {
                    gain: track.gain,
                    clips_signature: all_sorted_clips_signature
                }
            ).unwrap();
            hasher.update(track_with_hashed_children);
            tracks_signatures.push(format!("{:X}", hasher.finalize_reset()));
        }
        tracks_signatures.sort();  // Sort the tracks signatures by alphabetical order
        let all_sorted_tracks_signature = join_signatures(tracks_signatures);

        let audio_block_with_hashed_children = serde_json::to_string(
            &AudioBlockWithHashedChildren {
                tracks_signature: all_sorted_tracks_signature
            }
        ).unwrap();
        hasher.update(audio_block_with_hashed_children);
        audio_blocks_signatures.push(format!("{:X}", hasher.finalize_reset()));
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
    hasher.update(audio_project_with_hashed_children);
    let audio_project_signature = format!("{:X}", hasher.finalize_reset());

    println!("\nFinished hashing.\n  --execution_time:{}ms", (start.elapsed().as_micros() as f64 / 1000.0));
    audio_project_signature
}

fn join_signatures(signatures: Vec<String>) -> String {
    signatures.join("-")
}
