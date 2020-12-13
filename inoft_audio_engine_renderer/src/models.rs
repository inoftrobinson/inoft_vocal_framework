// pub const FORMAT_TYPE_WAV: &String = &String::from("wav");
// pub const FORMAT_TYPE_MP3: &String = &String::from("mp3");


use crate::audio_clip::AudioClip;
use std::cell::RefCell;

pub struct ReceivedTargetSpec {
    pub filepath: String,
    pub sample_rate: i32,
    pub format_type: String,
}

pub struct ReceivedParsedData {
    pub blocks: Vec<AudioBlock>,
    pub target_spec: ReceivedTargetSpec,
}

pub struct Time {
    pub type_key: String,
    pub relationship_parent_id: Option<String>,
    pub offset: Option<i16>,
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