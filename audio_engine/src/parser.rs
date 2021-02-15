use super::cpython::{Python, PyObject, ObjectProtocol, PyList, PyDict, PyString, PythonObject};
use crate::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip, Time};
use std::collections::HashMap;
use std::cell::RefCell;


pub fn parse_time_object(_py: Python, object_item: PyObject) -> Time {
    Time {
        type_key: object_item.get_item(_py, "type").unwrap().to_string(),
        relationship_parent_id: Some(object_item.get_item(_py, "relationship_parent_id").unwrap().to_string()),
        offset: Some(object_item.get_item(_py, "offset").unwrap().extract::<i16>(_py).unwrap()),
    }
}


pub fn parse_python(_py: Python, received_data: PyObject) -> ReceivedParsedData {
    let mut flattened_tracks_refs: HashMap<String, &Track> = HashMap::new();
    let mut flattened_audio_clips_refs: HashMap<String, &RefCell<AudioClip>> = HashMap::new();
    let mut audio_blocks_items: Vec<AudioBlock> = Vec::new();
    let audio_blocks_data: PyList = received_data.get_item(_py, "blocks").unwrap().extract::<PyList>(_py).unwrap();

    println!("blocks : {:?}", audio_blocks_data.len(_py));
    for i_block in 0..audio_blocks_data.len(_py) {
        let mut current_audio_block_tracks: Vec<Track> = Vec::new();

        let audio_block_data: PyObject = audio_blocks_data.get_item(_py, i_block);
        let tracks_data: PyDict = audio_block_data.get_item(_py, "tracks").unwrap().extract::<PyDict>(_py).unwrap();
        println!("tracks_data : {:?}", tracks_data.len(_py));

        //         for i_track in 0..tracks_data.len(_py) {
        for (track_id, track_data) in tracks_data.items(_py).iter() {
            let track_id = track_id.to_string();
            let mut current_track_clips: Vec<RefCell<AudioClip>> = Vec::new();
            let child_clips_data = track_data.get_item(_py, "clips").unwrap().extract::<PyDict>(_py).unwrap();

            for (clip_id, clip_data) in child_clips_data.items(_py).iter() {
                let clip_id = clip_data.get_item(_py, "id").unwrap().to_string();
                println!("{}", clip_data);

                let volume = match clip_data.get_item(_py, "volume") {
                    Ok(item) => { if item != _py.None() { Some(item.extract::<u8>(_py).unwrap()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let local_filepath = match clip_data.get_item(_py, "localFilepath") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let file_url = match clip_data.get_item(_py, "fileUrl") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };

                current_track_clips.push(AudioClip::new(
                    clip_id, local_filepath, file_url, volume,
                    parse_time_object(_py, clip_data.get_item(_py, "playerStartTime").unwrap()),
                    parse_time_object(_py, clip_data.get_item(_py, "playerEndTime").unwrap()),
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

    let target_spec_data = received_data.get_item(_py, "targetSpec").unwrap();
    let output_parsed_data = ReceivedParsedData {
        engine_account_id: match received_data.get_item(_py, "engineAccountId") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        },
        engine_project_id: match received_data.get_item(_py, "engineProjectId") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        },
        blocks: audio_blocks_items,
        target_spec: ReceivedTargetSpec {
            filepath: target_spec_data.get_item(_py, "filepath").unwrap().to_string(),
            sample_rate: target_spec_data.get_item(_py, "sampleRate").unwrap().extract::<i32>(_py).unwrap(),
            format_type: target_spec_data.get_item(_py, "formatType").unwrap().to_string(),
            export_target: target_spec_data.get_item(_py, "exportTarget").unwrap().to_string(),
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