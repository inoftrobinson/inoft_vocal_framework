#[cfg(test)]
mod tests {
    use crate::{append, AudioBlock, Track, AudioClip, Time, exporter};
    use crate::models::{ReceivedParsedData, ReceivedTargetSpec};
    use std::cell::RefCell;
    use tokio;
    use tokio::prelude::*;
    use std::collections::HashMap;
    use reqwest::Url;
    // use crate::hound2;
    use hound::WavReader;
    use std::io::{BufReader, Read};
    use tokio::fs;
    use std;
    use std::time::Instant;
    use crate::loader::{get_file_bytes_from_url, get_wave_reader_from_bytes};

    async fn resample() {
        let data = ReceivedParsedData {
            blocks: vec![
                AudioBlock {
                    tracks: vec![
                        Track {
                            track_id: String::from("track-1"),
                            child: vec![
                                AudioClip::new(
                                    String::from("clip-1"),
                                    Some("F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav".to_string()), None,
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
                                    0,
                                    0
                                ),
                                AudioClip::new(
                                    String::from("clip-2"),
                                    Some("F:/Sons utiles/70_Cm_ArpLoop_01_SP.wav".to_string()), None,
                                    Time {
                                        type_key: String::from("parent_start-time"),
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
                format_type: String::from("mp3"),
                export_target: String::from("managed-inoft-vocal-engine")
            }
        };
        let task_1 = tokio::spawn(exporter::get_upload_url(String::from("test.mp3"), 1000));
        let task_2 = tokio::spawn(append::main(data));
        let tasks = tokio::join!(task_1, task_2);
        println!("Finished tokio...");
    }

    #[test]
    fn resample_test() {
        let mut runtime = tokio::runtime::Runtime::new().unwrap();
        runtime.block_on(resample());
    }

    async fn get_file_from_url_old() {
        let start = Instant::now();

        let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/testgreat.mp3";
        let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/ambiance.wav";
        let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/output_final.wav";
        let client = reqwest::ClientBuilder::new().build().unwrap();
        let file_response = client
            .get(Url::parse(url).unwrap())
            .send().await.unwrap();

        let bytes = file_response.bytes().await.unwrap();
        let mut bytes_slice = &*bytes;
        println!("Took {}ms to retrieve the file", start.elapsed().as_millis());

        match std::str::from_utf8(bytes_slice) {
            Ok(v) => println!("Received text data, not good :/ : {}", v),
            Err(e) => println!("Received data was not text, its good ! {}", e),
        };

        let mut reader = BufReader::new(bytes_slice);
        let mut wav_reader = WavReader::new(reader).unwrap();
    }

    async fn get_file_from_url() {
        let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/output_final.wav";
        let bytes = get_file_bytes_from_url(url).await;
        let wave_reader = WavReader::new(BufReader::new(&*bytes)).unwrap();
    }

    #[test]
    fn get_file_from_url_test() {
        let mut runtime = tokio::runtime::Runtime::new().unwrap();
        runtime.block_on(get_file_from_url());
    }
}