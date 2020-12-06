use lame::Lame;
use claxon::FlacReader;
use std::fs::File;
use std::time::Instant;
use hyper::{Client, Uri, Method, Request, Body};
use hyper::client::HttpConnector;
use std::path::Path;
use std::io::Write;
use crate::models::ReceivedTargetSpec;
use std::borrow::{Borrow, BorrowMut};


async fn get_upload_url() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let client: Client<HttpConnector> = Client::new();
    let url: Uri = "http://127.0.0.1:5000/api/v1/@robinsonlabourdette/livetiktok/resources/project-audio-files/generate-presigned-upload-url"
        .parse()
        .unwrap();
    // assert_eq!(url.query(), Some("foo=bar"));
    let req = Request::builder()
        .method(Method::POST)
        .uri("http://127.0.0.1:5000/api/v1/@robinsonlabourdette/livetiktok/resources/project-audio-files/generate-presigned-upload-url")
        .header("content-type", "application/json")
        .body(Body::from(r#"{"library":"hyper"}"#))?;
    // client.request(req).and_then()
    let resp = client.request(req).await?;
    println!("Response: {}", resp.status());

    // let res = client.post(url).send().await;

    /*match client.get(url).await {
        Ok(res) => println!("Response: {}", res.status()),
        Err(err) => println!("Error: {}", err),
    };
     */
    Ok(())
}

// flac_song: &std::fs::File
pub async fn from_flac_to_mp3() -> Vec<u8> {
    let file = File::open("F:/Sons utiles/compressed-music.flac").expect("Error opening file");
    let mut flac_reader = FlacReader::new(file).expect("FlacReader error");
    let mut lame = Lame::new().expect("Coudn't create Lame");

    lame.set_channels(1).expect("Couldn't set num channels");
    /*lame.set_sample_rate(flac_reader.streaminfo().sample_rate as _)
        .expect("Couldn't set up sample rate");
     */
    lame.set_sample_rate(16000 as u32).expect("Couldn't set up sample rate");
    lame.set_channels(1).expect("Coudn't set up channels");
    lame.set_kilobitrate(48).expect("Coudn't set up kilobitrate");

    let mut left_samples: Vec<i16> = Vec::new();
    let mut right_samples: Vec<i16> = Vec::new();

    let mut frame_reader = flac_reader.blocks();
    loop {
        let frame: Vec<i32> = Vec::new();
        let result = frame_reader
            .read_next_or_eof(frame)
            .expect("error to read frame");

        match result {
            None => {
                break;
            }
            Some(block) => {
                let iter = block.stereo_samples();
                for (left, right) in iter {
                    left_samples.push(left as _);
                    right_samples.push(right as _);
                }
            }
        };
    }

    let num_samples = left_samples.len() as f64;
    let mp3_buffer_size = (1.25 * num_samples + 7200.0) as usize;

    let mut mp3_buffer = vec![0; mp3_buffer_size];

    lame.set_quality(4).expect("Set quality error");
    lame.init_params().expect("init parametrs error");

    println!("lame start");
    let start = Instant::now();
    let _ = lame.encode(
        left_samples.as_slice(),
        right_samples.as_slice(),
        mp3_buffer.as_mut_slice(),
    );
    println!("\nFinished lame.\n  --execution_time:{}ms", start.elapsed().as_millis());

    let res = get_upload_url().await;

    mp3_buffer
}

pub fn from_samples_to_mono_mp3(samples: Vec<i16>, target_spec: &ReceivedTargetSpec) -> Vec<u8> {
    let start = Instant::now();

    let mut lame = Lame::new().expect("Coudn't create Lame");
    lame.set_channels(1).expect("Couldn't set num channels");
    lame.set_sample_rate(target_spec.sample_rate as u32).expect("Couldn't set up sample rate");
    lame.set_kilobitrate(48).expect("Coudn't set up kilobitrate");
    // todo: make kilobitrate parametrable
    lame.set_quality(9).expect("Set quality error");
    // We set the quality to the 'worst' and fastest quality possible. With the formats used
    // by the inoft_vocal_framework, we do not hear the difference between the qualities.
    lame.init_params().expect("init parameters error");

    let num_samples = samples.len() as f64;
    let mp3_buffer_size = (num_samples + 7200.0) as usize;
    let mut mp3_buffer = vec![0; mp3_buffer_size];

    let samples_slice = samples.as_slice();
    let _ = lame.encode(
        samples_slice,
        samples_slice,
        mp3_buffer.as_mut_slice(),
    );

    let precision_divider = 100;
    let precision_samples_step = (target_spec.sample_rate / 100) as usize;
    println!(
        "\nRemoving trailing empty data from the mp3_buffer.\
        \n  --precision_divider:{}\n  --precision_samples_step:{}",
        precision_divider, precision_samples_step
    );
    let start_removing_trailing_empty_data = Instant::now();
    let mut mp3_buffer_inverted_index = mp3_buffer.len() - 1;
    while mp3_buffer_inverted_index > 0 {
        if mp3_buffer.get(mp3_buffer_inverted_index).unwrap() > &u8::MIN {
            mp3_buffer = mp3_buffer[0..mp3_buffer_inverted_index].to_owned();
            break;
        }
        mp3_buffer_inverted_index -= precision_samples_step;
    }
    println!("Finished removing of trailing empty data from the mp3_buffer.\n  --execution_time:{}ms", start_removing_trailing_empty_data.elapsed().as_millis());

    println!("\nFinished MP3 conversion using Lame.\n  --execution_time:{}ms", start.elapsed().as_millis());
    mp3_buffer
}

pub fn write_mp3_buffer_to_file(mp3_buffer: Vec<u8>, filepath: &str) {
    let path = Path::new(filepath);
    // Open a file in write-only mode, returns `io::Result<File>`
    let mut file = match File::create(&path) {
        Err(why) => panic!("couldn't create {:?}: {}", path, why),
        Ok(file) => file,
    };
    match file.write_all(mp3_buffer.as_slice()) {
        Err(why) => panic!("couldn't write to {:?}: {}", path, why),
        Ok(_) => println!("successfully wrote to {:?}", path),
    }
}