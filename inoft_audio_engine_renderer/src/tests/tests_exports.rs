#[cfg(test)]
mod tests {
    use crate::{render, append, exporter, AudioBlock, Track, AudioClip};
    use crate::models::{ReceivedParsedData, ReceivedTargetSpec};
    use cpython::PyObject;

    #[test]
    fn resample() {
        let data = ReceivedParsedData {
            blocks: vec![
                AudioBlock {
                    tracks: vec![
                        Track {
                            track_id: String::from("track-1"),
                            clips: vec![
                                AudioClip {
                                    clip_id: String::from("clip-1"),
                                    filepath: "F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav".to_string(),
                                    player_start_time: 0,
                                    player_end_time: 0,
                                    file_start_time: 0,
                                    file_end_time: 0
                                },
                                AudioClip {
                                    clip_id: String::from("clip-2"),
                                    filepath: "F:/Sons utiles/70_Cm_ArpLoop_01_SP.wav".to_string(),
                                    player_start_time: 0,
                                    player_end_time: 0,
                                    file_start_time: 0,
                                    file_end_time: 0
                                }
                            ],
                            gain: 0
                        }
                    ]
                }
            ],
            target_spec: ReceivedTargetSpec {
                filepath: String::from("F:/Sons utiles/tests/output_1.mp3"),
                sample_rate: 24000,
                format_type: String::from("mp3")
            }
        };
        append::main(data);
        assert_eq!(2 + 2, 4);
    }
}