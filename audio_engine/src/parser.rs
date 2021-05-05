use super::cpython::{Python, PyObject, ObjectProtocol, PyList, PyDict, PythonObject, PyBytes};
use crate::models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip, Time, ResampleSaveFileFromUrlData, ResampleSaveFileFromLocalFileData};
use std::collections::HashMap;
use std::cell::RefCell;
use audio_effects::base_transformer::BaseTransformer;
use audio_effects::tremolo::Tremolo;
use audio_effects::equalizer::EqualizerTransformer;


fn parse_time_object(_py: Python, object_item: PyObject) -> Time {
    Time {
        type_key: object_item.get_item(_py, "type").unwrap().to_string(),
        relationship_parent_id: Some(object_item.get_item(_py, "relationship_parent_id").unwrap().to_string()),
        offset: Some(object_item.get_item(_py, "offset").unwrap().extract::<f32>(_py).unwrap()),
    }
}

fn parse_target_spec(_py: Python, received_data: PyObject) -> ReceivedTargetSpec {
    let target_spec_data = received_data.get_item(_py, "targetSpec").unwrap();
    ReceivedTargetSpec {
        filepath: target_spec_data.get_item(_py, "filepath").unwrap().to_string(),
        sample_rate: target_spec_data.get_item(_py, "sampleRate").unwrap().extract::<u32>(_py).unwrap(),
        bitrate: target_spec_data.get_item(_py, "bitrate").unwrap().extract::<u16>(_py).unwrap(),
        num_channels: target_spec_data.get_item(_py, "numChannels").unwrap().extract::<u16>(_py).unwrap(),
        format_type: target_spec_data.get_item(_py, "formatType").unwrap().to_string(),
        export_target: target_spec_data.get_item(_py, "exportTarget").unwrap().to_string(),
    }
}


pub fn parse_python_render_call(_py: Python, received_data: PyObject) -> ReceivedParsedData {
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

        for (track_id, track_data) in tracks_data.items(_py).iter() {
            let track_id = track_id.to_string();
            let mut current_track_clips: Vec<RefCell<AudioClip>> = Vec::new();
            let child_clips_data = track_data.get_item(_py, "clips").unwrap().extract::<PyDict>(_py).unwrap();

            for (clip_id, clip_data) in child_clips_data.items(_py).iter() {
                let clip_id: String = clip_data.get_item(_py, "id").unwrap().to_string();
                println!("{}", clip_data);

                let volume: Option<u16> = match clip_data.get_item(_py, "volume") {
                    Ok(item) => { if item != _py.None() { Some(item.extract::<u16>(_py).unwrap()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let file_bytes: Option<Vec<u8>> = match clip_data.get_item(_py, "fileBytes") {
                    Ok(item) => { if item != _py.None() {
                        match item.extract::<PyBytes>(_py) {
                            Ok(bytes_object) => {
                                let bytes_data: &[u8] = bytes_object.data(_py);
                                Some(bytes_data.to_vec())
                                // We convert our array of bytes to a Vec, in order have a variable to which the Strict size at
                                // compile time does not apply to, and still be able to send back higher the ownership of the data.
                            } Err(err) => { None }
                        }
                    } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let local_filepath: Option<String> = match clip_data.get_item(_py, "localFilepath") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let file_url: Option<String> = match clip_data.get_item(_py, "fileUrl") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let file_start_time: f32 = match clip_data.get_item(_py, "fileStartTime") {
                    Ok(item) => { if item != _py.None() { item.extract::<f32>(_py).unwrap() } else { 0.0 } },
                    Err(err) => { println!("{:?}", err); 0.0 }
                };
                let file_end_time: Option<f32> = match clip_data.get_item(_py, "fileEndTime") {
                    Ok(item) => { if item != _py.None() { Some(item.extract::<f32>(_py).unwrap()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let effects: Option<PyList> = match clip_data.get_item(_py, "effects") {
                    Ok(item) => { if item != _py.None() { Some(item.extract::<PyList>(_py).unwrap()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };

                let mut effects_instances: Vec<Box<dyn BaseTransformer<i16>>> = vec![];
                if !effects.is_none() {
                    for effect_data in effects.unwrap().iter(_py) {
                        let effect_key: String = effect_data.get_item(_py, "key").unwrap().to_string();
                        let effect_parameters: PyDict = match effect_data.get_item(_py, "parameters") {
                            Ok(item) => { if item != _py.None() { item.extract::<PyDict>(_py).unwrap() } else { PyDict::new(_py) } },
                            Err(err) => { println!("{:?}", err); PyDict::new(_py) }
                        };
                        match effect_key.as_str() {
                            "tremolo" => {
                                let speed_parameter: f32 = effect_parameters.get_item(_py, "speed").unwrap().extract::<f32>(_py).unwrap();
                                let gain_parameter: f32 = effect_parameters.get_item(_py, "gain").unwrap().extract::<f32>(_py).unwrap();
                                effects_instances.push(Box::new(Tremolo::new(speed_parameter, gain_parameter)));
                            },
                            "equalizer" => {
                                // todo: pass curves
                                match EqualizerTransformer::new(Vec::new()) {
                                    Ok(effect) => { effects_instances.push(Box::new(effect)); },
                                    Err(err) => { println!("Error while instancing the equalizer transformer"); }
                                };
                            }
                            _ => { println!("Effect {} not supported", effect_key); }
                        }
                    }
                }

                current_track_clips.push(AudioClip::new(
                    clip_id, file_bytes, local_filepath, file_url, volume, effects_instances,
                    parse_time_object(_py, clip_data.get_item(_py, "playerStartTime").unwrap()),
                    parse_time_object(_py, clip_data.get_item(_py, "playerEndTime").unwrap()),
                    file_start_time, file_end_time,
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
        target_spec: parse_target_spec(_py, received_data)
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


pub fn parse_python_resample_from_file_url_call(_py: Python, data: PyObject) -> ResampleSaveFileFromUrlData {
    let file_url: String = data.get_item(_py, "fileUrl").unwrap().to_string();
    let target_spec = parse_target_spec(_py, data);
    ResampleSaveFileFromUrlData { file_url, target_spec }
}

pub fn parse_python_resample_from_local_file_call(_py: Python, data: PyObject) -> ResampleSaveFileFromLocalFileData {
    let source_filepath: String = data.get_item(_py, "sourceFilepath").unwrap().to_string();
    let target_spec = parse_target_spec(_py, data);
    ResampleSaveFileFromLocalFileData { source_filepath, target_spec }
}