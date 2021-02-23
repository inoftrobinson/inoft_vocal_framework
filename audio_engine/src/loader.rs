use std::time::Instant;
use reqwest::{Url, StatusCode};
use bytes::Bytes;
use std::fs::File;
use std::path::Path;
use std::io::{Write, Read};
use std::fs;
use std::env::current_exe;

/*
let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/testgreat.mp3";
let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/ambiance.wav";
let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/output_final.wav";
 */

pub async fn get_file_bytes_from_url(url: &str) -> Box<[u8]> {
    let start = Instant::now();
    let client = reqwest::ClientBuilder::new().build().unwrap();
    let file_response = client
        .get(Url::parse(url).unwrap())
        .send().await.unwrap();

    let bytes: Bytes = file_response.bytes().await.unwrap() as Bytes;
    let bytes_boxed = bytes.to_vec().into_boxed_slice();
    println!("Took {}ms to retrieve the file at url : {}", start.elapsed().as_millis(), url);

    match std::str::from_utf8(&*bytes_boxed) {
        Ok(v) => println!("Received text data, not good :/ : {}", v),
        Err(e) => println!("Received data was not text, its good ! {}", e),
    };
    // todo: return none if there has been an error and that the received data is some text data
    bytes_boxed
}

/*
pub async fn get_file_bytes_from_url(url: &str) -> Bytes {
    let start = Instant::now();

    println!("{:?}", current_exe());
    let paths = fs::read_dir("/mnt/files").unwrap();
    for path in paths {
        println!("Name: {}", path.unwrap().path().display())
    }

    let filename = url.split("/").last().unwrap();
    let expected_efs_filepath = format!("/mnt/files/{}", filename);
    let expected_efs_path = Path::new(&expected_efs_filepath);
    if expected_efs_path.exists() {
        println!("Retrieving {} from efs files...", filename);
        let mut file = File::open(expected_efs_path).unwrap();
        let mut buffer: Vec<u8> = Vec::new();
        file.read_to_end(&mut buffer).expect("error while reading file");
        println!("Took {}ms to retrieve the file from efs : {}", start.elapsed().as_millis(), url);
        buffer
    } else {
        let client = reqwest::ClientBuilder::new().build().unwrap();
        let file_response = client
            .get(Url::parse(url).unwrap())
            .send().await.unwrap();

        let bytes: Bytes = file_response.bytes().await.unwrap() as Bytes;
        let bytes_vec = bytes.to_vec();
        let bytes_slice = &*bytes;
        println!("Took {}ms to retrieve the file at url : {}", start.elapsed().as_millis(), url);

        println!("Writing to file ! :)");
        let mut file = match File::create(&expected_efs_filepath) {
            Err(why) => panic!("couldn't create {:?}: {}", expected_efs_filepath, why),
            Ok(file) => file,
        };
        match file.write_all(bytes_slice) {
            Err(why) => panic!("couldn't write to {:?}: {}", expected_efs_filepath, why),
            Ok(_) => println!("successfully wrote to {:?}", expected_efs_filepath),
        }

        match std::str::from_utf8(&bytes_slice) {
            Ok(v) => println!("Received text data, not good :/ : {}", v),
            Err(e) => println!("Received data was not text, its good ! {}", e),
        };
        // todo: return none if there has been an error and that the received data is some text data
        bytes
    }
}
 */

pub async fn file_exist_at_url(url: &str) -> bool {
    let start = Instant::now();
    let client = reqwest::ClientBuilder::new().build().unwrap();
    let file_response = client
        .head(Url::parse(url).unwrap())
        .send().await.unwrap();

    println!("Took {}ms to check if file exist at url : {}", start.elapsed().as_millis(), url);
    match file_response.status() { StatusCode::OK => true, _ => false }
}
