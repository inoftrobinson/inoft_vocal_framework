mod append;
mod resampler;
mod renderer;
mod exporter;
// mod s3;

use std::f32::consts::PI;
use std::i16;
use hound;
use hound::WavReader;
use hound::WavSamples;
use std::io::BufReader;
use std::fs::File;
use std::ptr::null;


/*
fn write_sinewave(filepath: &str) {
    let spec = hound::WavSpec {
        channels: 1,
        sample_rate: 44100,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };
    let mut writer = hound::WavWriter::create(filepath, spec).unwrap();
    for t in (0 .. 44100).map(|x| x as f32 / 44100.0) {
        let sample = (t * 440.0 * 2.0 * PI).sin();
        let amplitude = i16::MAX as f32;
        writer.write_sample((sample * amplitude) as i16).unwrap();
    }
}
 */


/*
fn open_wav_file(filepath: &str) -> WavReader<BufReader<File>> {
    let mut reader = WavReader::open(filepath).unwrap();
    reader

    /*println!("Opened");
    let v = reader.samples::<i16>();
    v*/
    // &v
}
 */

/*
fn square(mut reader: WavReader<BufReader<File>>) {
    println!("Opened");
    let sqr_sum = reader.samples::<i16>().fold(0.0, |sqr_sum, s| {
        let sample = s.unwrap() as f64;
        // println!("{}", sample);
        sqr_sum + sample * sample;
        sqr_sum
    });
    println!("RMS is {}", (sqr_sum / reader.len() as f64).sqrt());
}
 */

/*
fn change_volume(mut reader: WavReader<BufReader<File>>) {
    let sqr_sum = reader.samples::<i16>().for_each(0.0, |sqr_sum, s| {
        let sample = s.unwrap() as f64;
        println!("{}", sample);
        sqr_sum + sample * sample;
        sqr_sum
    });
    println!("RMS is {}", (sqr_sum / reader.len() as f64).sqrt());
}
 */

/*async fn upload() {
    let e = s3::upload().await;
}*/

fn main() {
    exporter::from_flac_to_mp3();
    append::main();
    /*

    let arr: [u32; 5] = [1, 2, 3, 4, 5];
    for item in arr.iter() {
        println!("{}", item);
    }

    let money = 100000;
    println!("Is rich : {}", money > 1000);

    let value = 2000;
    println!("{v}", v=value);
    println!("Hello, world!");

    write_sinewave("F:/Sons utiles/sine.wav");
    change_volume(WavReader::open("F:/Sons utiles/test1.wav").unwrap());
     */
}