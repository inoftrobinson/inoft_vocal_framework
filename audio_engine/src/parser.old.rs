use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use crate::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip, Time};
use std::collections::HashMap;
use std::cell::RefCell;
use pyo3::types::{PyList, PyDict};


pub fn parse_time_object(object_item: &PyAny) -> Time {
    Time {
        type_key: object_item.get_item("type").unwrap().to_string(),
        relationship_parent_id: Some(object_item.get_item("relationship_parent_id").unwrap().to_string()),
        offset: Some(object_item.get_item("offset").unwrap().extract::<i16>().unwrap()),
    }
}


pub fn parse_python(_py: Python, received_data: PyAny) -> ReceivedParsedData {
    let data_dict: &PyDict = received_data.downcast().unwrap();

    let mut flattened_tracks_refs: HashMap<String, &Track> = HashMap::new();
    let mut flattened_audio_clips_refs: HashMap<String, &RefCell<AudioClip>> = HashMap::new();
    let mut audio_blocks_items: Vec<AudioBlock> = Vec::new();
    let audio_blocks_data: &PyList = data_dict.get_item("blocks").unwrap().downcast::<PyList>().unwrap();

    println!("blocks : {:?}", audio_blocks_data.len());
    for i_block in 0..audio_blocks_data.len() {
        let mut current_audio_block_tracks: Vec<Track> = Vec::new();

        let audio_block_data: &PyDict = audio_blocks_data.get_item(i_block as isize).downcast::<PyDict>().unwrap();
        let tracks_data: &PyDict = audio_block_data.get_item("tracks").unwrap().downcast::<PyDict>().unwrap();
        println!("tracks_data : {:?}", tracks_data.len());

        //         for i_track in 0..tracks_data.len(_py) {
        for (track_id, track_data) in tracks_data.iter() {  // .items().iter() {
            let track_id = track_id.to_string();
            let track_data: &PyDict = track_data.downcast::<PyDict>().unwrap();

            let mut current_track_clips: Vec<RefCell<AudioClip>> = Vec::new();
            let child_clips_data = track_data.get_item("clips").unwrap().downcast::<PyDict>().unwrap();

            for (clip_id, clip_data) in child_clips_data.iter() {
                let clip_data: &PyDict = clip_data.downcast::<PyDict>().unwrap();
                let clip_id = clip_data.get_item("id").unwrap().to_string();
                println!("{}", clip_data);

                let volume = match clip_data.get_item("volume") {
                    Some(item) => { if !item.is_none() { Some(item.extract::<u8>().unwrap()) } else { None } },
                    None => { None }
                };
                let local_filepath = match clip_data.get_item("localFilepath") {
                    Some(item) => { if !item.is_none() { Some(item.to_string()) } else { None } },
                    None => { None }
                };
                let file_url = match clip_data.get_item("fileUrl") {
                    Some(item) => { if !item.is_none() { Some(item.to_string()) } else { None } },
                    None => { None }
                };

                current_track_clips.push(AudioClip::new(
                    clip_id, local_filepath, file_url, volume,
                    parse_time_object(clip_data.get_item("playerStartTime").unwrap()),
                    parse_time_object(clip_data.get_item("playerEndTime").unwrap()),
                    0,
                    0,
                ));
            }
            println!("{:?}", track_data);
            
            current_audio_block_tracks.push(Track {
                track_id,
                clips: current_track_clips,
                gain: 0
            });
        }

        audio_blocks_items.push(AudioBlock {
            tracks: current_audio_block_tracks
        });
    }

    let target_spec_data = data_dict.get_item("targetSpec").unwrap();
    let output_parsed_data = ReceivedParsedData {
        engine_account_id: match data_dict.get_item("engineAccountId") {
            Some(item) => { if !item.is_none() { Some(item.to_string()) } else { None } },
            None => { None }
        },
        engine_project_id: match data_dict.get_item("engineProjectId") {
            Some(item) => { if !item.is_none() { Some(item.to_string()) } else { None } },
            None => { None }
        },
        blocks: audio_blocks_items,
        target_spec: ReceivedTargetSpec {
            filepath: target_spec_data.get_item("filepath").unwrap().to_string(),
            sample_rate: target_spec_data.get_item("sampleRate").unwrap().extract::<i32>().unwrap(),
            format_type: target_spec_data.get_item("formatType").unwrap().to_string(),
            export_target: target_spec_data.get_item("exportTarget").unwrap().to_string(),
        },
    };

    for audio_block in output_parsed_data.blocks.iter() {
        let tracks = &audio_block.tracks;
        for track in tracks.iter() {
            flattened_tracks_refs.insert(String::from(&track.track_id), track);
            for clip in track.clips.iter() {
                flattened_audio_clips_refs.insert(String::from(&clip.borrow().clip_id), clip);
            }
        }
    }
    for track_ref in flattened_tracks_refs.iter() {
        println!("id:{} & gain:{:?}", track_ref.0, track_ref.1.gain);
    }
    for clip_ref in flattened_audio_clips_refs.iter() {
        println!("id:{} & filepath:{:?}", clip_ref.0, clip_ref.1.borrow().filepath);
    }

    output_parsed_data
}