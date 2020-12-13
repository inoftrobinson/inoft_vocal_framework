use crate::models::{ReceivedParsedData, Track};
use std::time::Instant;
use hound::{WavReader};
use std::io::BufReader;
use std::fs::File;
use std::num::Wrapping;
use std::borrow::{Borrow, BorrowMut};


pub fn render_to_vec(data: &ReceivedParsedData) -> Vec<i16> {
    let start = Instant::now();

    let mut out_samples: Vec<i16> = Vec::new();
    let mut files_readers: Vec<WavReader<BufReader<File>>> = vec![];
    let mut duration_longest_file_buffer: u32 = 0;
    let mut file_reader_longest_file: Option<&WavReader<BufReader<File>>> = None;

    // The inoft_audio_engine_renderer has been optimized and tested to render audio with 16 bits per sample.
    // Changing this value to 24 (the only other possible setting), could cause unexpected behaviors.
    let target_spec = hound::WavSpec {
        channels: 1,
        sample_rate: data.target_spec.sample_rate as u32,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };

    if data.blocks.len() > 0 {
        let mut first_audio_block = data.blocks.get(0).unwrap();
        let mut borrowed_first_audio_block = first_audio_block.borrow_mut();
        let mut first_track = borrowed_first_audio_block.tracks.get(0).unwrap();
        let borrowed_first_track = first_track.borrow_mut();
        let audio_clips = &borrowed_first_track.clips;

        /*let track = Track {
            track_id: "".to_string(),
            clips: vec![],
            gain: 0
        };
        let mut trackRef = &mut &track;
        borrowed_first_track = trackRef;
        borrowed_first_track.clips[0].filepath = "".to_string();
         */
        // todo: fix that and support multiple audio blocks instead of just using the first one

        for (i_file, audio_clip) in audio_clips.iter().enumerate() {
            let mut audio_clip = audio_clips.get(i_file).unwrap().borrow_mut();
            audio_clip.resample(target_spec);

            let outing_start = Instant::now();
            println!("start_time: {:?}", audio_clip.player_start_time.offset);
            let start_sample = audio_clip.render_player_start_time_to_sample_index(target_spec.sample_rate);
            let end_sample = audio_clip.render_player_end_time_to_sample_index(target_spec.sample_rate);
            let audio_clip_resamples = audio_clip.resamples.as_ref().unwrap();

            for i_sample in 0..audio_clip_resamples.len() {
                // todo: fix issue where if the first sound has a player_start_time more than
                //  zero, it will be pushed in the out_samples like if it had no player_start_time.
                let current_sample_index = i_sample + start_sample;
                if out_samples.len() > current_sample_index + 1 {
                    out_samples[current_sample_index] = (Wrapping(out_samples[current_sample_index]) + Wrapping(audio_clip_resamples[i_sample])).0;
                } else {
                    out_samples.push(audio_clip_resamples[i_sample]);
                }
            }
            println!("\nFinished outing.\n  --execution_time:{}ms", outing_start.elapsed().as_millis());

            /*
            files_readers.push(file_reader);
            let mut current_file_reader = &files_readers[i_file];

            println!("current spec = {:?}", current_file_reader.spec());
            println!("{}", current_file_reader.duration());
            println!("{:?}", current_file_reader.spec());
            let current_file_duration = current_file_reader.duration();
            if current_file_duration > duration_longest_file_buffer {
                duration_longest_file_buffer = current_file_duration;
                file_reader_longest_file = Some(current_file_reader);
            }
             */
        }
    }

    println!("Total rendering time : {}ms", start.elapsed().as_millis());
    out_samples
}