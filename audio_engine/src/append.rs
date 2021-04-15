use std::time::Instant;
use crate::models::{ReceivedParsedData};
use crate::exporter::{from_samples_to_mono_mp3, write_mp3_buffer_to_file, get_upload_url, post_mp3_buffer_to_s3_with_presigned_url};
use crate::renderer::Renderer;
use std::mem::{size_of};
use crate::saver;
use crate::tracer::TraceItem;
use self::hound::Error;

extern crate hound;


pub async fn main(trace: &mut TraceItem, data: ReceivedParsedData, expected_render_file_hash: String) -> Result<Option<String>, hound::Error> {
    let trace_rendering_samples = trace.create_child(String::from("Render samples"));
    let rendered_samples = Renderer::render(trace_rendering_samples, &data).await;
    trace_rendering_samples.close();

    let trace_saving_samples = trace.create_child(String::from("Saving samples"));
    let file_url = saver::save_samples(
        trace_saving_samples, rendered_samples,
        &data.target_spec, expected_render_file_hash
    ).await;
    trace_saving_samples.close();

    file_url
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