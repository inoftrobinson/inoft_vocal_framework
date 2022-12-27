use super::cpython::{Python, PyObject, ObjectProtocol, PyList, PyDict, PythonObject, PyBytes};
use crate::models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip, Time, ResampleSaveFileFromUrlData, ResampleSaveFileFromLocalFileData, EngineApiData, TracingData};
use std::collections::HashMap;
use std::cell::RefCell;
use audio_effects::base_transformer::BaseTransformer;
use audio_effects::tremolo::Tremolo;
use audio_effects::equalizer::EqualizerTransformer;


fn parse_tracing_data(_py: Python, received_data: &PyObject) -> TracingData {
    TracingData {
        output_filepath: match received_data.get_item(_py, "tracingOutputFilepath") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        },
        output_url: match received_data.get_item(_py, "tracingOutputUrl") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        }
    }
}

fn parse_engine_api_data(_py: Python, received_data: &PyObject) -> EngineApiData {
    let override_engine_base_url: Option<String> = match received_data.get_item(_py, "overrideEngineBaseUrl") {
        Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } }, Err(_) => { None }
    };
    EngineApiData {
        engine_base_url: override_engine_base_url.unwrap_or(String::from("https://www.engine.inoft.com")),
        engine_account_id: match received_data.get_item(_py, "engineAccountId") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        },
        engine_project_id: match received_data.get_item(_py, "engineProjectId") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        },
        access_token: match received_data.get_item(_py, "engineAccessToken") {
            Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
            Err(err) => { println!("{:?}", err); None }
        },
    }
}


fn parse_time_object(_py: Python, object_item: PyObject) -> Time {
    let type_key: String = object_item.get_item(_py, "type").unwrap().to_string();
    let relationship_parent_id: Option<String> = match object_item.get_item(_py, "relationship_parent_id") {
        Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } }, Err(_) => None
    };
    let offset: Option<f32> = match object_item.get_item(_py, "offset") {
        Ok(item) => { if item != _py.None() { Some(item.extract::<f32>(_py).unwrap()) } else { None } }, Err(_) => None
    };
    Time { type_key, relationship_parent_id, offset }
}

fn parse_target_spec(_py: Python, received_data: &PyObject) -> ReceivedTargetSpec {
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
    // let mut flattened_tracks_refs: HashMap<String, &Track> = HashMap::new();
    let mut audio_blocks_items: Vec<AudioBlock> = Vec::new();
    let audio_blocks_data: PyList = received_data.get_item(_py, "blocks").unwrap().extract::<PyList>(_py).unwrap();

    for i_block in 0..audio_blocks_data.len(_py) {
        let mut current_audio_block_tracks: Vec<Track> = Vec::new();

        let audio_block_data: PyObject = audio_blocks_data.get_item(_py, i_block);
        let tracks_data: PyDict = audio_block_data.get_item(_py, "tracks").unwrap().extract::<PyDict>(_py).unwrap();

        for (track_id, track_data) in tracks_data.items(_py).iter() {
            let track_id = track_id.to_string();
            let mut current_track_clips: Vec<RefCell<AudioClip>> = Vec::new();
            let child_clips_data = track_data.get_item(_py, "clips").unwrap().extract::<PyDict>(_py).unwrap();

            for (clip_id, clip_data) in child_clips_data.items(_py).iter() {
                let clip_id: String = clip_data.get_item(_py, "id").unwrap().to_string();
                let clip_type: String = clip_data.get_item(_py, "type").unwrap().to_string();

                // Special attributes of file type clip's
                let file_bytes: Option<Vec<u8>> = match clip_data.get_item(_py, "fileBytes") {
                    Ok(item) => {
                        if item != _py.None() {
                            match item.extract::<PyBytes>(_py) {
                                Ok(bytes_object) => {
                                    let bytes_data: &[u8] = bytes_object.data(_py);
                                    Some(bytes_data.to_vec())
                                    // We convert our array of bytes to a Vec, in order have a variable to which the Strict size at
                                    // compile time does not apply to, and still be able to send back higher the ownership of the data.
                                }
                                Err(_) => None
                            }
                        } else { None }
                    },
                    Err(_) => None
                };
                let local_filepath: Option<String> = match clip_data.get_item(_py, "localFilepath") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let file_url: Option<String> = match clip_data.get_item(_py, "fileUrl") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };

                // Special attributes of speech type clip's
                let text: Option<String> = match clip_data.get_item(_py, "text") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };
                let voice_key: Option<String> = match clip_data.get_item(_py, "voiceKey") {
                    Ok(item) => { if item != _py.None() { Some(item.to_string()) } else { None } },
                    Err(err) => { println!("{:?}", err); None }
                };

                let volume: Option<u16> = match clip_data.get_item(_py, "volume") {
                    Ok(item) => { if item != _py.None() { Some(item.extract::<u16>(_py).unwrap()) } else { None } },
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
                    clip_id, clip_type,
                    file_bytes, local_filepath, file_url,
                    text, voice_key,
                    volume, effects_instances,
                    parse_time_object(_py, clip_data.get_item(_py, "playerStartTime").unwrap()),
                    parse_time_object(_py, clip_data.get_item(_py, "playerEndTime").unwrap()),
                    file_start_time, file_end_time,
                ));
            }
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

    ReceivedParsedData {
        engine_api_data: parse_engine_api_data(_py, &received_data),
        target_spec: parse_target_spec(_py, &received_data),
        blocks: audio_blocks_items,
        tracing: parse_tracing_data(_py, &received_data)
    }
    /*
    let mut flattened_audio_clips_refs: HashMap<String, &RefCell<AudioClip>> = HashMap::new();
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
     */
}


pub fn parse_python_resample_from_file_url_call(_py: Python, data: PyObject) -> ResampleSaveFileFromUrlData {
    let file_url: String = data.get_item(_py, "fileUrl").unwrap().to_string();
    let target_spec = parse_target_spec(_py, &data);
    let engine_api_data = parse_engine_api_data(_py, &data);
    ResampleSaveFileFromUrlData { engine_api_data, target_spec, file_url }
}

pub fn parse_python_resample_from_local_file_call(_py: Python, data: PyObject) -> ResampleSaveFileFromLocalFileData {
    let source_filepath: String = data.get_item(_py, "sourceFilepath").unwrap().to_string();
    let target_spec = parse_target_spec(_py, &data);
    let engine_api_data = parse_engine_api_data(_py, &data);
    ResampleSaveFileFromLocalFileData { engine_api_data, target_spec, source_filepath }
}