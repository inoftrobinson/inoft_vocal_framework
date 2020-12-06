#[cfg(test)]
mod tests {
    use crate::{append, AudioBlock, Track, AudioClip, Time};
    use crate::models::{ReceivedParsedData, ReceivedTargetSpec};

    #[test]
    fn resample() {
        let data = ReceivedParsedData {
            blocks: vec![
                AudioBlock {
                    tracks: vec![
                        Track {
                            track_id: String::from("track-1"),
                            clips: vec![
                                AudioClip::new(
                                    String::from("clip-1"),
                                    "F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav".to_string(),
                                    Time {
                                        type_key: String::from("track_start-time"),
                                        relationship_parent_id: Some(String::from("track-1")),
                                        offset: None
                                    },
                                    Time {
                                        type_key: String::from("until-self-end"),
                                        relationship_parent_id: None,
                                        offset: None
                                    },
                                    0,
                                    0
                                ),
                                AudioClip::new(
                                    String::from("clip-2"),
                                    "F:/Sons utiles/70_Cm_ArpLoop_01_SP.wav".to_string(),
                                    Time {
                                        type_key: String::from("track_start-time"),
                                        relationship_parent_id: Some(String::from("track-1")),
                                        offset: Some(20)
                                    },
                                    Time {
                                        type_key: String::from("until-self-end"),
                                        relationship_parent_id: None,
                                        offset: None
                                    },
                                    0, 0
                                )
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