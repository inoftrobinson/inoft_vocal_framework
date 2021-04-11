use crate::models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip, Time};

pub fn make_sample_project_data() -> ReceivedParsedData {
    let data = ReceivedParsedData {
        blocks: vec![
            AudioBlock {
                tracks: vec![
                    Track {
                        track_id: String::from("track-1"),
                        clips: vec![
                             AudioClip::new(
                                String::from("clip-1"),
                                None,
                                Some("F:/Sons utiles/Musics/Vintage (1940s) French Music/La Vie en Rose - Edith Piaf - Louiguy - Luypaerts.mp3".to_string()),
                                None,
                                Some(100),
                                Time {
                                    type_key: String::from("parent_start-time"),
                                    relationship_parent_id: Some(String::from("track-1")),
                                    offset: None
                                },
                                Time {
                                    type_key: String::from("until-self-end"),
                                    relationship_parent_id: None,
                                    offset: None
                                },
                                0.0,
                                None
                            ),
                            AudioClip::new(
                                String::from("clip-1"),
                                None,
                                Some("F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav".to_string()),
                                None,
                                Some(100),
                                Time {
                                    type_key: String::from("parent_start-time"),
                                    relationship_parent_id: Some(String::from("track-1")),
                                    offset: None
                                },
                                Time {
                                    type_key: String::from("until-self-end"),
                                    relationship_parent_id: None,
                                    offset: None
                                },
                                0.0,
                                None
                            ),
                            AudioClip::new(
                                String::from("clip-2"),
                                None,
                                Some("F:/Sons utiles/70_Cm_ArpLoop_01_SP.wav".to_string()),
                                None,
                                Some(100),
                                Time {
                                    type_key: String::from("parent_start-time"),
                                    relationship_parent_id: Some(String::from("track-1")),
                                    offset: Some(20.0)
                                },
                                Time {
                                    type_key: String::from("until-self-end"),
                                    relationship_parent_id: None,
                                    offset: None
                                },
                                0.0,
                                None
                            )
                        ],
                        gain: 0,
                    }
                ]
            }
        ],
        target_spec: ReceivedTargetSpec {
            filepath: String::from("F:/Sons utiles/tests/output_1.mp3"),
            sample_rate: 24000,
            bitrate: 16,
            num_channels: 1,
            format_type: String::from("mp3"),
            export_target: String::from("managed-inoft-vocal-engine")
        },
        engine_account_id: Some(String::from("b1fe5939-032b-462d-92e0-a942cd445096")),
        engine_project_id: Some(String::from("22ac1d08-292d-4f2e-a9e3-20d181f1f58f"))
    };
    data
}
