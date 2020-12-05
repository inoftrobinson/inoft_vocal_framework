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
                            clips: vec![
                                AudioClip {
                                    filepath: "F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav".to_string(),
                                    player_start_time: 0,
                                    player_end_time: 0,
                                    file_start_time: 0,
                                    file_end_time: 0
                                },
                                AudioClip {
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
                sample_rate: 24000
            }
        };
        // let target_spec = &data.target_spec;
        exporter::from_samples_to_mono_mp3(append::main(data), &ReceivedTargetSpec {
            sample_rate: 24000
        });

        assert_eq!(2 + 2, 4);
    }
}