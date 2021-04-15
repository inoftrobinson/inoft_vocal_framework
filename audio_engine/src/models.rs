use std::cell::RefCell;
use serde::{Serialize, Deserialize};
pub use crate::audio_clip::AudioClip;


pub struct ReceivedTargetSpec {
    pub filepath: String,
    pub sample_rate: u32,
    pub bitrate: u16,
    pub num_channels: u16,
    pub format_type: String,
    pub export_target: String,
}

impl ReceivedTargetSpec {
    pub fn to_wav_spec(&self) -> hound::WavSpec {
        // The 16 value for the bits_per_sample is hardcoded and cannot be changed. The sample_rate
        // is only used for mp3 or other files types export, but never for wav exports.
        hound::WavSpec {
            channels: self.num_channels,
            sample_rate: self.sample_rate,
            bits_per_sample: 16,
            sample_format: hound::SampleFormat::Int
        }
    }
}

pub struct ReceivedParsedData {
    pub engine_account_id: Option<String>,
    pub engine_project_id: Option<String>,
    pub blocks: Vec<AudioBlock>,
    pub target_spec: ReceivedTargetSpec,
}

pub struct ResampleSaveFileFromUrlData {
    pub file_url: String,
    pub target_spec: ReceivedTargetSpec
}

pub struct ResampleSaveFileFromLocalFileData {
    pub source_filepath: String,
    pub target_spec: ReceivedTargetSpec
}


#[derive(Clone, Serialize, Deserialize)]
pub struct Time {
    pub type_key: String,
    pub relationship_parent_id: Option<String>,
    pub offset: Option<f32>,
}

pub struct Track {
    pub track_id: String,
    pub clips: Vec<RefCell<AudioClip>>,
    pub gain: i16,
}

impl Track {
    pub fn new_empty() -> Track {
        Track { track_id: String::from("static"), clips: Vec::new(), gain: 0 }
    }
    /*pub fn push_clip(&self, audio_clip: AudioClip) {
        self.clips.borrow_mut().push(audio_clip);
    }
    pub fn add_clip(&self, audio_clip: AudioClip) {
        let mut mutable_clips = self.clips.borrow_mut();
        mutable_clips.push(audio_clip);
        // mutable_clips.last().unwrap()
    }*/
}

pub struct AudioBlock {
    pub tracks: Vec<Track>,
}

impl AudioBlock {
    pub fn new_empty() -> AudioBlock {
        AudioBlock { tracks: Vec::new() }
    }
    /*pub fn add_track(&self, track: Track) {
        let mut mutable_tracks = self.tracks.borrow_mut();
        mutable_tracks.push(RefCell::new(track));
    }*/
}