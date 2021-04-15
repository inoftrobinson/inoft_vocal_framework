use crate::exporter::{write_mp3_buffer_to_file, from_samples_to_mono_mp3, post_mp3_buffer_to_s3_with_presigned_url, get_upload_url};
use crate::models::ReceivedTargetSpec;
use std::mem::size_of;
use crate::tracer::TraceItem;
use std::io::BufWriter;
use hound::{Error, WavWriter};
use std::fs::File;


pub async fn save_samples(trace: &mut TraceItem, samples: Vec<i16>, target_spec: &ReceivedTargetSpec, desired_filename: String) -> Result<Option<String>, hound::Error> {
    match &*target_spec.format_type {
        "mp3" => {
            let mp3_buffer = from_samples_to_mono_mp3(samples, target_spec);
            match &*target_spec.export_target {
                "local" => {
                    println!("Writing mp3_buffer to file...");
                    write_mp3_buffer_to_file(mp3_buffer, &*target_spec.filepath);
                    Ok(None)
                },
                "managed-inoft-vocal-engine" => {
                    println!("Uploading mp3_buffer to managed inoft-vocal-engine....");
                    let mp3_buffer_expected_bytes_size = mp3_buffer.capacity() * size_of::<u8>();
                    println!("expected bytes size : {}", mp3_buffer_expected_bytes_size);

                    let upload_url_data = get_upload_url(
                        format!("{}.mp3", desired_filename),
                        mp3_buffer_expected_bytes_size
                    ).await.expect("Error connecting to engine API")
                        .expect("Error connecting to engine API");
                    Ok(Some(post_mp3_buffer_to_s3_with_presigned_url(mp3_buffer, upload_url_data).await))
                }
                _ => {
                    panic!("Export target not supported");
                    // todo: return error instead of panicking
                }
            }
        },
        "wav" => {
            let wav_target_spec = target_spec.to_wav_spec();
            let e = match hound::WavWriter::create(&target_spec.filepath, wav_target_spec) {
                Ok(mut writer) => {
                    for sample in samples {
                        writer.write_sample(sample).unwrap();
                    }
                    Ok(Some(String::from("F:/Inoft/file.wav")))
                },
                Err(err) => {
                    println!("Wav writer error : {}", err);
                    Err(err)
                }
            };
            e
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