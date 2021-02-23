use std::time::Instant;
use reqwest::{Url, StatusCode};
use bytes::Bytes;
use std::fs::File;
use std::path::Path;
use std::io::Write;

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
    let bytes_slice = &*bytes;
    println!("Took {}ms to retrieve the file at url : {}", start.elapsed().as_millis(), url);

    let expected_filepath = format!("/mnt/files/{}", url);
    if !Path::new(&expected_filepath).exists() {
        println!("Writing to file ! :)");
        File::create(expected_filepath).unwrap().write_all(bytes_slice);
    }

    match std::str::from_utf8(&bytes_slice) {
        Ok(v) => println!("Received text data, not good :/ : {}", v),
        Err(e) => println!("Received data was not text, its good ! {}", e),
    };
    // todo: return none if there has been an error and that the received data is some text data
    bytes
}

pub async fn file_exist_at_url(url: &str) -> bool {
    let start = Instant::now();
    let client = reqwest::ClientBuilder::new().build().unwrap();
    let file_response = client
        .head(Url::parse(url).unwrap())
        .send().await.unwrap();

    println!("Took {}ms to check if file exist at url : {}", start.elapsed().as_millis(), url);
    match file_response.status() { StatusCode::OK => true, _ => false }
}
