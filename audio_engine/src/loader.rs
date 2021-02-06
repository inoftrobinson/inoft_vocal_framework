use std::time::Instant;
use reqwest::Url;
use std::io::{BufReader};
use hound::WavReader;
use bytes::Bytes;

/*
let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/testgreat.mp3";
let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/ambiance.wav";
let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/output_final.wav";
 */

pub async fn get_file_bytes_from_url(url: &str) -> Bytes {
    let start = Instant::now();
    let client = reqwest::ClientBuilder::new().build().unwrap();
    let file_response = client
        .get(Url::parse(url).unwrap())
        .send().await.unwrap();

    let bytes: Bytes = file_response.bytes().await.unwrap() as Bytes;
    let mut bytes_slice = &*bytes;
    println!("Took {}ms to retrieve the file at url : {}", start.elapsed().as_millis(), url);

    match std::str::from_utf8(&bytes_slice) {
        Ok(v) => println!("Received text data, not good :/ : {}", v),
        Err(e) => println!("Received data was not text, its good ! {}", e),
    };
    // todo: return none if there has been an error and that the received data is some text data
    bytes
}
