// pub const FORMAT_TYPE_WAV: &String = &String::from("wav");
// pub const FORMAT_TYPE_MP3: &String = &String::from("mp3");


use std::cell::{Cell, RefCell};

pub struct ReceivedTargetSpec {
    pub filepath: String,
    pub sample_rate: i32,
    pub format_type: String,
}

pub struct ReceivedParsedData {
    pub blocks: Vec<AudioBlock>,
    pub target_spec: ReceivedTargetSpec,
}

pub struct AudioClip {
    pub clip_id: String,
    pub filepath: String,
    pub player_start_time: i16,
    pub player_end_time: i16,
    pub file_start_time: i16,
    pub file_end_time: i16,
}

pub struct Track {
    pub track_id: String,
    pub clips: Vec<AudioClip>,
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

impl AudioClip {
    fn new(filepath: &str, player_start_time: Option<i16>, player_end_time: Option<i16>,
           file_start_time: Option<i16>, file_end_time: Option<i16>) -> AudioClip {
        AudioClip {
            clip_id: String::from("static-id"),
            filepath: String::from(filepath),
            player_start_time: player_start_time.unwrap_or(0),
            player_end_time: player_end_time.unwrap_or(0),
            file_start_time: file_start_time.unwrap_or(0),
            file_end_time: file_end_time.unwrap_or(0)
        }
    }

    fn without_args(filepath: &str) -> AudioClip {
        AudioClip::new(filepath, None, None, None, None)
    }
}