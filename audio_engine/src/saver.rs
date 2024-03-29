use crate::exporter::{write_mp3_buffer_to_file, from_samples_to_mono_mp3, post_buffer_to_s3_with_presigned_url, get_upload_url, write_wav_samples_to_file};
use crate::models::{ReceivedTargetSpec, ReceivedParsedData, EngineApiData};
use std::mem::size_of;
use crate::tracer::TraceItem;
use std::io::BufWriter;
use hound::{WavWriter};
use std::fs::File;
use std::error::Error;


pub async fn save_samples(
    trace: &mut TraceItem,
    target_spec: &ReceivedTargetSpec, engine_api_data: &EngineApiData,
    samples: Vec<i16>, desired_filename: String
) -> Result<String, Box<dyn Error>> {

    match &*target_spec.format_type {
        "mp3" => {
            let mp3_buffer = from_samples_to_mono_mp3(trace, samples, target_spec);
            match &*target_spec.export_target {
                "local" => {
                    println!("Writing mp3_buffer to file...");
                    let trace_write_mp3_buffer_to_file = trace.create_child(String::from("Write MP3 buffer to file"));
                    let writing_result = write_mp3_buffer_to_file(mp3_buffer, &*target_spec.filepath);
                    trace_write_mp3_buffer_to_file.close();
                    writing_result
                },
                "managed-inoft-vocal-engine" => {
                    println!("Uploading mp3_buffer to managed inoft-vocal-engine....");
                    let trace_upload_mp3_buffer_to_inoft_vocal_engine = trace.create_child(
                        String::from("Upload MP3 buffer to Inoft Vocal Engine")
                    );
                    let mp3_buffer_expected_bytes_size = mp3_buffer.len() * size_of::<u8>();
                    let upload_url_data = get_upload_url(
                        engine_api_data,
                        format!("{}.mp3", desired_filename),
                        mp3_buffer_expected_bytes_size
                    ).await
                        .expect("Error connecting to engine API")
                        .expect("Error connecting to engine API");
                    let result = Ok(post_buffer_to_s3_with_presigned_url(mp3_buffer, upload_url_data).await);
                    trace_upload_mp3_buffer_to_inoft_vocal_engine.close();
                    result
                }
                _ => {
                    panic!("Export target not supported");
                    // todo: return error instead of panicking
                }
            }
        },
        "wav" => {
            let wav_target_spec = target_spec.to_wav_spec();
            match &*target_spec.export_target {
                "local" => {
                    println!("Writing wav samples to file....");
                    let trace_write_wav_samples_to_file = trace.create_child(String::from("Write WAV samples to file"));
                    let result = write_wav_samples_to_file(samples, wav_target_spec, &target_spec.filepath);
                    trace_write_wav_samples_to_file.close();
                    result
                },
                "managed-inoft-vocal-engine" => {
                    println!("Uploading wav_buffer to managed inoft-vocal-engine....");
                    let buffer: Vec<u8> = samples.into_iter().map(|s| s.to_be_bytes().to_vec()).flatten().collect::<Vec<u8>>();
                    // todo: finish the wav export to engine
                    // let buffer: Vec<u8> = samples.into_iter().map(|s| s as u8).collect::<Vec<u8>>();
                    let buffer_expected_bytes_size = buffer.len() * size_of::<u8>();
                    let upload_url_data = get_upload_url(
                        engine_api_data,
                        format!("{}.wav", desired_filename),
                        buffer_expected_bytes_size
                    ).await
                        .expect("Error connecting to engine API")
                        .expect("Error connecting to engine API");
                    Ok(post_buffer_to_s3_with_presigned_url(buffer, upload_url_data).await)
                }
                _ => {
                    panic!("Export target not supported");
                    // todo: return error instead of panicking
                }
            }
        },
        _ => {
            panic!(
                "Format type not supported. Only 'mp3' and 'wav' formats are supported to export audio.\
                \n  --request_format_type:{}", target_spec.format_type
            );
            // todo: return error instead of panicking
        }
    }
}