#[cfg(test)]
mod tests {
    use crate::{append, AudioBlock, Track, AudioClip, Time, exporter};
    use crate::models::{ReceivedParsedData, ReceivedTargetSpec};
    use std::cell::RefCell;
    use tokio;
    use tokio::prelude::*;
    use hyper::{Client, Uri, Method, Request, Body};
    use hyper::client::HttpConnector;
    use std::collections::HashMap;

    async fn resample() {
        let data = ReceivedParsedData {
            blocks: vec![
                AudioBlock {
                    tracks: vec![
                        Track {
                            track_id: String::from("track-1"),
                            clips: vec![
                                RefCell::new(AudioClip::new(
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
                                )),
                                RefCell::new(AudioClip::new(
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
                                ))
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
        tokio::runtime::Handle::current().spawn(exporter::get_upload_url());
        // tokio::runtime::Handle::current().spawn(append::main(data));
        println!("Finished tokio...");
        // assert_eq!(2 + 2, 4);
    }

    #[test]
    fn resample_test() {
        let mut rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(resample());
    }

    async fn do_request() {
        let client = Client::new();
        // let url: Uri = "http://httpbin.org/response-headers?foo=bar"
        let url: Uri = "http://127.0.0.1:5000/api/v1/@robinsonlabourdette/livetiktok/resources/project-audio-files/generate-presigned-upload-url"
            .parse()
            .unwrap();

        match client.get(url).await {
            Ok(res) => println!("Response: {}", res.status()),
            Err(err) => println!("Error: {}", err),
        }
    }

    async fn test_http_request_app() -> Result<(), Box<dyn std::error::Error>> {
        let resp = reqwest::get("https://httpbin.org/ip").await?.json::<HashMap<String, String>>().await?;
        println!("{:#?}", resp);
        Ok(())

            /*
        let client = Client::new();
        // let url: Uri = "http://httpbin.org/response-headers?foo=bar"
        let url: Uri = "http://127.0.0.1:5000/api/v1/@robinsonlabourdette/livetiktok/resources/project-audio-files/generate-presigned-upload-url"
            .parse()
            .unwrap();

        match client.get(url).await {
            Ok(res) => println!("Response: {}", res.status()),
            Err(err) => println!("Error: {}", err),
        }

             */
    }

    #[test]
    fn test_http_request() {
        let mut rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(test_http_request_app());
    }
}