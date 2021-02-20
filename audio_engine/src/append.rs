use std::path::Path;
use std::time::Instant;
use crate::{ReceivedParsedData};
use crate::exporter::{from_samples_to_mono_mp3, write_mp3_buffer_to_file, get_upload_url, post_mp3_buffer_to_s3_with_presigned_url};
use crate::renderer::Renderer;
use std::mem::{size_of};

extern crate hound;


pub async fn main(data: ReceivedParsedData, expected_render_file_hash: String) -> Result<Option<String>, ()> {
    let start = Instant::now();

    let path: &Path = data.target_spec.filepath.as_ref();
    let target_spec = &data.target_spec;
    let rendered_samples = Renderer::render(&data).await;

    let writing_start = Instant::now();
    println!("format type : {}", target_spec.format_type);
    let file_url = match &*target_spec.format_type {
        "mp3" => {
            let mp3_buffer = from_samples_to_mono_mp3(rendered_samples, target_spec);
            match &*target_spec.export_target {
                "local" => {
                    println!("Writing mp3_buffer to file...");
                    write_mp3_buffer_to_file(mp3_buffer, &*target_spec.filepath);
                    None
                },
                "managed-inoft-vocal-engine" => {
                    println!("Uploading mp3_buffer to managed inoft-vocal-engine....");
                    let mp3_buffer_expected_bytes_size = mp3_buffer.capacity() * size_of::<u8>();
                    println!("expected bytes size : {}", mp3_buffer_expected_bytes_size);

                    let upload_url_data = get_upload_url(
                    format!("{}.mp3", expected_render_file_hash),
                    mp3_buffer_expected_bytes_size
                    ).await.expect("Error connecting to engine API")
                        .expect("Error connecting to engine API");
                    Some(post_mp3_buffer_to_s3_with_presigned_url(mp3_buffer, upload_url_data).await)
                }
                _ => {
                    panic!("Export target not supported");
                }
            }
        },
        "wav" => {
            let wav_target_spec = hound::WavSpec {
                channels: 1,
                sample_rate: target_spec.sample_rate as u32,
                bits_per_sample: 16,
                sample_format: hound::SampleFormat::Int,
            };
            let mut writer =  hound::WavWriter::create(path, wav_target_spec).unwrap();
            for i_sample in 0..rendered_samples.len() {
                writer.write_sample(rendered_samples[i_sample]).unwrap();
            }
            None
        },
        _ => {
            panic!(
                "Format type not supported. Only 'mp3' and 'wav' formats are supported to export audio.\
                \n  --request_format_type:{}", target_spec.format_type
            );
        }
    };
    println!("\nFinished conversion and writing.\n  --execution_time:{}ms", writing_start.elapsed().as_millis());
    println!("\nFinished rendering, conversion and writing.\n  --execution_time:{}ms", start.elapsed().as_millis());
    Ok(file_url)
    // writer.finalize().unwrap();

    /*for (i_reader, mut file_reader) in files_readers.iter().enumerate() {
        let sample_rate = file_reader.spec().sample_rate as i32;
        let samples: WavSamples<BufReader<File>, i16> = file_reader.samples();
        let resamples = resample(samples, sample_rate, TARGET_SPEC.sample_rate as i32);
        for i_sample in 0..resamples.len() {
            writer.write_sample(resamples[i_sample]).unwrap();
        }
    }
    // println!("{}", duration_longest_file_buffer / file_reader_longest_file.unwrap().spec().sample_rate);
    // let samples: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
    // let samples1: Vec<i16> = files_readers[0].samples().map(|s| s.unwrap()).collect();
    let samples2: Vec<i16> = files_readers[1].samples().map(|s| s.unwrap()).collect();
    println!("spec : {:?}", files_readers[0].spec());
    // println!("{:?}", samples2);
     */

    /*
    if files_paths.len() > 0 {
        for filepath in files_paths.iter() {
            let current_file_reader = WavReader::open(filepath).unwrap();

            let current_file_duration = current_file_reader.duration();
            if current_file_duration > duration_longest_file_buffer {
                duration_longest_file_buffer = current_file_duration;
                file_reader_longest_file = Some(current_file_reader);
            }
            // files_readers.push(current_file_reader);
        }
        // println!("{}", duration_longest_file_buffer / file_reader_longest_file.unwrap().spec().sample_rate);
    }
    */
}