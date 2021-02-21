use symphonia::core::probe::Hint;
use symphonia::core::io::{ReadOnlySource, MediaSourceStream, BitStreamLtr, ByteStream, BitStream, BufStream};
use symphonia::core::units::{Duration, Time};
use std::path::Path;
use std::fs::File;
use symphonia::core::formats::{FormatOptions};
use symphonia::core::meta::MetadataOptions;
use symphonia::core::codecs::DecoderOptions;
use symphonia::core::errors::Error;
use crate::loader::get_file_bytes_from_url;
use std::io;
use std::io::{BufReader, BufWriter, Write, Cursor};
use log::{error, info, warn};
use std::borrow::{Borrow, BorrowMut};
use symphonia::core::audio::{AudioBufferRef, SignalSpec, SampleBuffer};

mod decoder_utils;
use bincode;
use hound::{WavSamples, WavReader, WavWriter};
use serde_json::to_writer;
use bytes::buf::ext::Writer;
use bytes::Bytes;
use symphonia_core::sample::SampleFormat;
use symphonia_core::codecs::CodecParameters;
use symphonia_core::formats::SeekTo;

pub fn get_file_extension_from_file_url(file_url: &str) -> Option<&str> {
    file_url.split(".").last()
}

pub async fn decode_from_file_url(file_url: &str, file_start_time: i16, limit_time_to_load: Option<i16>) -> (Option<Vec<i16>>, Option<CodecParameters>) {
    let mut hint = Hint::new();
    let file_extension = get_file_extension_from_file_url(file_url).expect("No file extension found");
    hint.with_extension(file_extension);

    let file_bytes = get_file_bytes_from_url(file_url).await;
    let boxed_file_bytes = file_bytes.to_vec().into_boxed_slice();
    let media_source_cursor = Cursor::new(boxed_file_bytes.clone());
    let mut media_source_stream = MediaSourceStream::new(Box::new(media_source_cursor));
    decode(media_source_stream, hint, file_start_time, limit_time_to_load)
}

pub fn decode_from_local_filepath(filepath: &str, file_start_time: i16, limit_time_to_load: Option<i16>) -> (Option<Vec<i16>>, Option<CodecParameters>) {
    let mut hint = Hint::new();
    let path = Path::new(filepath);
    if let Some(extension) = path.extension() {
        if let Some(extension_str) = extension.to_str() {
            hint.with_extension(extension_str);
        }
    }
    let file_source = Box::new(File::open(path).unwrap());
    let media_source_stream = MediaSourceStream::new(file_source);
    decode(media_source_stream, hint, file_start_time, limit_time_to_load)
}

pub fn decode(media_source_stream: MediaSourceStream, hint: Hint, file_start_time: i16, limit_time_to_load: Option<i16>) -> (Option<Vec<i16>>, Option<CodecParameters>) {
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

            // Decode all packets, ignoring decode errors.
            let file_start_sample_index = file_start_time as usize * stream_sample_rate as usize;
            let index_stop_samples_load = if limit_time_to_load.is_none() { usize::MAX } else {
                file_start_sample_index + (limit_time_to_load.unwrap() as usize * stream_sample_rate as usize)
            };

            let mut all_samples: Vec<i16> = Vec::new();
            let mut index: usize = 0;
            loop {
                match reader.next_packet() {
                    Err(_err) => break,
                    Ok(packet) => {
                        match decoder.decode(&packet) {
                            Err(Error::DecodeError(err)) => {
                                warn!("decode error: {}", err);
                                continue;
                            },
                            Err(_err) => break,
                            Ok(decoded) => {
                                if index < file_start_sample_index {
                                    index += decoded.capacity();
                                } else if index <= index_stop_samples_load {
                                    let spec = *decoded.spec();
                                    let capacity = decoded.capacity();
                                    let duration = Duration::from(capacity as u64);

                                    let mut sample_buffer = SampleBuffer::<i16>::new(duration, spec);
                                    sample_buffer.copy_interleaved_ref(decoded);
                                    all_samples.extend(sample_buffer.samples());
                                    index += capacity;
                                } else {
                                    println!("Breaked loading of samples at index {}", index);
                                    break
                                }
                                continue
                            }
                        }
                    }
                }
            };
            decoder.close();

            println!("decoder samples length : {}", all_samples.len());
            (Some(all_samples), Some(stream_codec_params))
            /*else {
            // todo: when using a file start time or file end time that trim the file duration, only seek the data that will be used
                // Playback mode.
                pretty_print_format(path_str, &probed);

                // Seek to the desired timestamp if requested.
                if let Some(seek_value) = matches.value_of("seek") {
                    let pos = seek_value.parse::<f64>().unwrap_or(0.0);
                    probed.format.seek(SeekTo::Time{ time: Time::from(pos) }).unwrap();
                }

                // Set the decoder options.
                let options = DecoderOptions {
                    verify: matches.is_present("verify"),
                    ..Default::default()
                };
            };*/
        }
        Err(err) => {
            // The input was not supported by any format reader.
            error!("File not supported. reason? {}", err);
            println!("File not supported. reason? {}", err);
            (None, None)
        }
    }
}
