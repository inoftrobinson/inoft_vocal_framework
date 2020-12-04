use lame::Lame;
use claxon::FlacReader;
use std::fs::File;
use std::time::Instant;
use hyper::{Client, Uri, Method, Request, Body};
use hyper::client::HttpConnector;


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

    lame.set_channels(1)
        .expect("Couldn't set num channels");
    /*lame.set_sample_rate(flac_reader.streaminfo().sample_rate as _)
        .expect("Couldn't set up sample rate");
     */
    lame.set_sample_rate(16000 as u32)
        .expect("Couldn't set up sample rate");
    lame.set_channels(1)
        .expect("Coudn't set up channels");
    lame.set_kilobitrate(48)
        .expect("Coudn't set up kilobitrate");

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


/*pub fn export_to_mp3() {
    /*let lame_ = Lame::new();
    let mut lame = lame_.unwrap();
    lame.set_sample_rate(16000);
    lame.encode(&[10 as i16, 20 as i16], &[10 as i16, 20 as i16], &mut [2 as u8]);
     */

    /*int read, write;

    FILE *pcm = fopen("file.pcm", "rb");
    FILE *mp3 = fopen("file.mp3", "wb");

    const int PCM_SIZE = 8192;
    const int MP3_SIZE = 8192;

    short int pcm_buffer[PCM_SIZE*2];
    unsigned char mp3_buffer[MP3_SIZE];

    lame_t lame = lame_init();
    lame_set_in_samplerate(lame, 44100);
    lame_set_VBR(lame, vbr_default);
    lame_init_params(lame);

    do {
        read = fread(pcm_buffer, 2*sizeof(short int), PCM_SIZE, pcm);
        if (read == 0)
            write = lame_encode_flush(lame, mp3_buffer, MP3_SIZE);
        else
            write = lame_encode_buffer_interleaved(lame, pcm_buffer, read, mp3_buffer, MP3_SIZE);
        fwrite(mp3_buffer, write, 1, mp3);
    } while (read != 0);

    lame_close(lame);
    fclose(mp3);
    fclose(pcm);

    return 0;
     */
}

 */