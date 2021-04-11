use std::fs::File;
use std::io::{Write, Cursor};
use std::path::Path;
use log::{error, info, warn};

use symphonia::core::probe::Hint;
use symphonia::core::io::MediaSourceStream;
use symphonia::core::units::{Duration};
use symphonia::core::formats::FormatOptions;
use symphonia::core::meta::MetadataOptions;
use symphonia::core::codecs::DecoderOptions;
use symphonia::core::errors::Error;
use symphonia_core::codecs::CodecParameters;
use symphonia::core::audio::SampleBuffer;

mod decoder_utils;
use crate::loader::get_file_bytes_from_url;
use crate::tracer::TraceItem;


pub fn decode_from_bytes(
    trace: &mut TraceItem, bytes: Box<[u8]>, file_extension: String,
    file_start_time: f32, limit_time_to_load: Option<f32>
) -> (Option<Vec<i16>>, Option<CodecParameters>) {

    let mut hint = Hint::new();
    hint.with_extension(&*file_extension);
    let trace_file_loading = trace.create_child(String::from("File bytes loading"));
    let media_source_cursor = Cursor::new(bytes);
    let media_source_stream = MediaSourceStream::new(Box::new(media_source_cursor));
    trace_file_loading.close();

    decode(trace, media_source_stream, hint, file_start_time, limit_time_to_load)
}


pub fn decode_from_local_filepath(
    trace: &mut TraceItem, filepath: &str,
    file_start_time: f32, limit_time_to_load: Option<f32>
) -> (Option<Vec<i16>>, Option<CodecParameters>) {

    let mut hint = Hint::new();
    let path = Path::new(filepath);
    if let Some(extension) = path.extension() {
        if let Some(extension_str) = extension.to_str() {
            hint.with_extension(extension_str);
        }
    }
    let trace_file_opening = trace.create_child(String::from("File opening"));
    let file_source = Box::new(File::open(path).unwrap());
    let media_source_stream = MediaSourceStream::new(file_source);
    trace_file_opening.close();

    decode(trace, media_source_stream, hint, file_start_time, limit_time_to_load)
}

pub fn get_file_extension_from_file_url(file_url: &str) -> Option<&str> {
    file_url.split(".").last()
}

pub async fn decode_from_file_url(
    trace: &mut TraceItem, file_url: &str,
    file_start_time: f32, limit_time_to_load: Option<f32>
) -> (Option<Vec<i16>>, Option<CodecParameters>) {

    /*let filename = file_url.split("/").last().unwrap();
    let expected_efs_filepath = format!("/mnt/files/{}", filename);
    let expected_efs_path = Path::new(&expected_efs_filepath);*/
    /* if false && expected_efs_path.exists() {
        decode_from_local_filepath(trace, &*expected_efs_filepath, file_start_time, limit_time_to_load)
    } else {*/
    // todo: try to find the file from the efs drive, otherwise write it to it
    let mut hint = Hint::new();
    let file_extension = get_file_extension_from_file_url(file_url).expect("No file extension found");
    hint.with_extension(file_extension);

    let trace_file_retrieving = trace.create_child(String::from("File bytes retrieving"));
    let boxed_file_bytes = get_file_bytes_from_url(file_url).await;
    trace_file_retrieving.close();

    /*let trace_writing_retrieved_file_to_local_storage = trace.create_child(String::from("Writing retrieved file to local storage"));
    let mut file = match File::create(&expected_efs_filepath) {
        Err(why) => panic!("couldn't create {:?}: {}", expected_efs_filepath, why),
        Ok(file) => file,
    };
    match file.write_all(&*boxed_file_bytes) {
        Err(why) => panic!("couldn't write to {:?}: {}", expected_efs_filepath, why),
        Ok(_) => println!("successfully wrote to {:?}", expected_efs_filepath),
    }
    trace_writing_retrieved_file_to_local_storage.close();*/

    let trace_bytes_conversion_to_stream = trace.create_child(String::from("Bytes conversion to stream"));
    let media_source_cursor = Cursor::new(boxed_file_bytes.clone());
    let media_source_stream = MediaSourceStream::new(Box::new(media_source_cursor));
    trace_bytes_conversion_to_stream.close();

    decode(trace, media_source_stream, hint, file_start_time, limit_time_to_load)
}

fn decode(
    trace: &mut TraceItem, media_source_stream: MediaSourceStream,
    hint: Hint, file_start_time: f32, limit_time_to_load: Option<f32>
) -> (Option<Vec<i16>>, Option<CodecParameters>) {

    let trace_decoding = trace.create_child(String::from("decoding"));

    // Use the default options for metadata and format readers.
    let format_opts: FormatOptions = Default::default();
    let metadata_opts: MetadataOptions = Default::default();

    // Probe the media source stream for metadata and get the format reader.
    match symphonia::default::get_probe().format(&hint, media_source_stream, &format_opts, &metadata_opts) {
        Ok(probed) => {
            let mut reader = probed.format;

            let decode_options = DecoderOptions { verify: false, ..Default::default() };
            let stream = reader.default_stream().unwrap();
            let stream_codec_params = stream.codec_params.clone();
            let stream_sample_rate = stream_codec_params.sample_rate.unwrap();
            decoder_utils::pretty_print_stream(stream, 0);

            let mut decoder = symphonia::default::get_codecs().make(&stream_codec_params, &decode_options).unwrap();

            let file_start_sample_index = file_start_time as usize * stream_sample_rate as usize;
            let index_stop_samples_load = if limit_time_to_load.is_none() { usize::MAX } else {
                file_start_sample_index + (limit_time_to_load.unwrap() as usize * stream_sample_rate as usize)
            };

            // In order to find out how much samples there is per packet, we can either try to replicate the inner
            // sophisticated logic of the symphonia library, which would be the most performant, but would mean a lot
            // of code to maintain, since depending on the file formats, encoding, sample rates, channels, etc, we can
            // have various values. Or, we can have a dumber approach, is to always decode the first packet of a clip,
            // check the num of samples for it, and then use it in the packet loop. We just to not forget to initialize
            // the index to the index_increment instead of the 0 (to make count the first next_buffer) and to add the
            // samples for the first_sample_buffer if need to. PS : yes, we could compute the increment in the packet
            // loop itself, but it would be very complicated, because if the first index is below the file_start_sample_index,
            // we would never have decoded a packet, so we would not yet have initialized our index_increment, so we would either
            // need to add a special case to decode a packet in the "if index < file_start_sample_index {" condition, or we would
            // need to decode the packet on each iteration of the loop, which would make no sense for the case where we do not intend to
            // add the decoded samples inside the all_samples vector. To resume, this approach is ugly, but performant and easy to maintain.
            let first_audio_buffer = decoder.decode(&reader.next_packet().unwrap()).unwrap();
            let first_audio_buffer_spec = first_audio_buffer.spec();
            let first_audio_buffer_num_channels = first_audio_buffer_spec.channels.count();
            let first_audio_buffer_duration = Duration::from(first_audio_buffer.capacity() as u64);
            let mut first_sample_buffer = SampleBuffer::<i16>::new(first_audio_buffer_duration, *first_audio_buffer_spec);
            first_sample_buffer.copy_interleaved_ref(first_audio_buffer);
            let index_increment = first_sample_buffer.samples().len() / first_audio_buffer_num_channels;
            // The only manual adjustment we need to make not handled by our little system, is to divide the num of samples by the num of channels.

            let mut all_samples: Vec<i16> = Vec::new();
            let mut index: usize = index_increment;

            if index <= index_stop_samples_load {
                all_samples.extend(first_sample_buffer.samples());
            }
            loop {
                // Decode all packets, ignoring decode errors.
                match reader.next_packet() {
                    Err(_err) => break,
                    Ok(packet) => {
                        match decoder.decode(&packet) {
                            Err(Error::DecodeError(err)) => {
                                warn!("Decoding error: {}", err);
                                continue;
                            },
                            Err(_err) => break,
                            Ok(decoded) => {
                                if index < file_start_sample_index {
                                    index += index_increment;
                                    continue;
                                } else if index <= index_stop_samples_load {
                                    let spec = *decoded.spec();
                                    let capacity = decoded.capacity();
                                    let duration = Duration::from(capacity as u64);

                                    let mut sample_buffer = SampleBuffer::<i16>::new(duration, spec);
                                    sample_buffer.copy_interleaved_ref(decoded);
                                    all_samples.extend(sample_buffer.samples());
                                    index += index_increment;
                                    continue;
                                } else {
                                    println!("Broken loading of samples at index {}", index);
                                    break;
                                }
                            }
                        }
                    }
                }
            };
            decoder.close();

            println!("decoder samples length : {}", all_samples.len());
            trace_decoding.close();
            (Some(all_samples), Some(stream_codec_params))
        }
        Err(err) => {
            // The input was not supported by any format reader.
            error!("File not supported. reason? {}", err);
            println!("File not supported. reason? {}", err);
            trace_decoding.close();
            (None, None)
        }
    }
}

