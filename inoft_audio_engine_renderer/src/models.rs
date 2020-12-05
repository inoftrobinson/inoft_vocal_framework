// pub const FORMAT_TYPE_WAV: &String = &String::from("wav");
// pub const FORMAT_TYPE_MP3: &String = &String::from("mp3");


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
    pub filepath: String,
    pub player_start_time: i16,
    pub player_end_time: i16,
    pub file_start_time: i16,
    pub file_end_time: i16,
}

pub struct Track {
    pub clips: Vec<AudioClip>,
    pub gain: i16,
}

pub struct AudioBlock {
    pub tracks: Vec<Track>,
}

impl AudioClip {
    fn new(filepath: &str, player_start_time: Option<i16>, player_end_time: Option<i16>,
           file_start_time: Option<i16>, file_end_time: Option<i16>) -> AudioClip {
        AudioClip {
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