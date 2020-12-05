use cpython::{PyResult, Python, py_module_initializer, py_fn, PyObject, ObjectProtocol, PyList, PyDict};
use crate::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip};


pub fn parse_python(_py: Python, received_data: PyObject) -> ReceivedParsedData {
    let audio_blocks_data: PyList = received_data.get_item(_py, "blocks").unwrap().extract::<PyList>(_py).unwrap();
    let mut audio_blocks_items: Vec<AudioBlock> = Vec::new();
    println!("blocks : {:?}", audio_blocks_data.len(_py));
    for i_block in 0..audio_blocks_data.len(_py) {
        let audio_block_data: PyObject = audio_blocks_data.get_item(_py, i_block);
        let tracks_data: PyList = audio_block_data.get_item(_py, "tracks").unwrap().extract::<PyList>(_py).unwrap();
        let mut tracks_items: Vec<Track> = Vec::new();
        println!("tracks_data : {:?}", tracks_data.len(_py));
        for i_track in 0..tracks_data.len(_py) {
            let current_track_data = tracks_data.get_item(_py, i_track);
            let clips_data = current_track_data.get_item(_py, "clips").unwrap().extract::<PyDict>(_py).unwrap();
            let mut clips_items: Vec<AudioClip> = Vec::new();
            for (clip_id, clip_item) in clips_data.items(_py).iter() {
                let current_clip_data = clips_data.get_item(_py, clip_id).unwrap();
                println!("{}", clip_item);
                clips_items.push(AudioClip {
                    filepath: current_clip_data.get_item(_py, "localFilepath").unwrap().to_string(),
                    player_start_time: 0,
                    player_end_time: 0,
                    file_start_time: 0,
                    file_end_time: 0
                });
            }
            tracks_items.push(Track {
                clips: clips_items,
                gain: 0
            });
            println!("{:?}", current_track_data);
        }
        audio_blocks_items.push(AudioBlock {
            tracks: tracks_items
        });
    }

    let target_spec_data = received_data.get_item(_py, "targetSpec").unwrap();
    ReceivedParsedData {
        blocks: audio_blocks_items,
        target_spec: ReceivedTargetSpec {
            filepath: target_spec_data.get_item(_py, "filepath").unwrap().to_string(),
            sample_rate: target_spec_data.get_item(_py, "sampleRate").unwrap().extract::<i32>(_py).unwrap(),
            format_type: target_spec_data.get_item(_py, "formatType").unwrap().to_string(),
        },
    }
}