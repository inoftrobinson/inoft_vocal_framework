use symphonia::core::probe::ProbeResult;
use symphonia::core::formats::{Cue, Stream};
use symphonia::core::meta::{Tag, Visual, ColorMode};

/*pub fn pretty_print_format(path: &str, probed: &ProbeResult) {
    println!("+ {}", path);
    pretty_print_streams(probed.format.streams());

    // Prefer metadata that's provided in the container format, over other tags found during the
    // probe operation.
    if let Some(metadata) = probed.format.metadata().current() {
        pretty_print_tags(metadata.tags());
        pretty_print_visuals(metadata.visuals());

        // Warn that certain tags are preferred.
        if probed.metadata.current().is_some() {
            info!("tags that are part of the container format are preferentially printed.");
            info!("not printing additional tags that were found while probing.");
        }
    }
    else if let Some(metadata) = probed.metadata.current() {
        pretty_print_tags(metadata.tags());
        pretty_print_visuals(metadata.visuals());
    }

    pretty_print_cues(probed.format.cues());
    println!("-");
}*/

pub fn pretty_print_stream(stream: &Stream, idx: usize) {
    let params = &stream.codec_params;

    println!("Stream {} data : ", idx);
    if let Some(codec) = symphonia::default::get_codecs().get_codec(params.codec) {
        println!("    --codec: {} ({})", codec.long_name, codec.short_name);
    }

    if let Some(sample_rate) = params.sample_rate {
        println!("    --sample_rate: {}", sample_rate);
    }
    if let Some(n_frames) = params.n_frames {
        println!("    --n_frames: {}", n_frames);
    }
    if let Some(max_frames_per_packet) = params.max_frames_per_packet {
        println!("    --max_frames_per_packet: {}", max_frames_per_packet);
    }
    if let Some(sample_format) = params.sample_format {
        println!("    --sample_format: {:?}", sample_format);
    }
    if let Some(bits_per_sample) = params.bits_per_sample {
        println!("    --bits_per_sample: {}", bits_per_sample);
    }
    if let Some(bits_per_coded_sample) = params.bits_per_coded_sample {
        println!("    --bits_per_coded_sample: {}", bits_per_coded_sample);
    }
    if let Some(channels) = params.channels {
        println!("    --channels.count(): {}", channels.count());
        println!("    --channels (map): {}", channels);
    }
    if let Some(channel_layout) = params.channel_layout {
        println!("    --channel_layout: {:?}", channel_layout);
    }
    if let Some(extra_data) = &params.extra_data {
        println!("    --extra_data: {:?}", extra_data);
    }
    if let Some(leading_padding) = &params.leading_padding {
        println!("    --leading_padding: {}", leading_padding);
    }
    if let Some(trailing_padding) = &params.trailing_padding {
        println!("    --trailing_padding: {}", trailing_padding);
    }
    println!("    --packet_data_integrity: {}", params.packet_data_integrity);
    if let Some(time_base) = &params.time_base {
        println!("    --time_base: {:?}", time_base);
    }
    if let Some(language) = &stream.language {
        println!("    --language: {}", language);
    }
}

pub fn pretty_print_streams(streams: &[Stream]) {
    if !streams.is_empty() {
        println!("|");
        println!("| // Streams //");

        for (idx, stream) in streams.iter().enumerate() {
            pretty_print_stream(stream, idx);
        }
    }
}

/*
pub fn pretty_print_cues(cues: &[Cue]) {
    if !cues.is_empty() {
        println!("|");
        println!("| // Cues //");

        for (idx, cue) in cues.iter().enumerate() {
            println!("|     [{:0>2}] Track:      {}", idx + 1, cue.index);
            println!("|          Timestamp:  {}", cue.start_ts);

            // Print tags associated with the Cue.
            if !cue.tags.is_empty() {
                println!("|          Tags:");

                for (tidx, tag) in cue.tags.iter().enumerate() {
                    if let Some(std_key) = tag.std_key {
                        println!("{}", pretty_print_tag_item(tidx + 1, &format!("{:?}", std_key), &tag.value, 21));
                    }
                    else {
                        println!("{}", pretty_print_tag_item(tidx + 1, &tag.key, &tag.value, 21));
                    }
                }
            }

            // Print any sub-cues.
            if !cue.points.is_empty() {
                println!("|          Sub-Cues:");

                for (ptidx, pt) in cue.points.iter().enumerate() {
                    println!("|                      [{:0>2}] Offset:    {:?}", ptidx + 1, pt.start_offset_ts);

                    // Start the number of sub-cue tags, but don't print them.
                    if !pt.tags.is_empty() {
                        println!("|                           Sub-Tags:  {} (not listed)", pt.tags.len());
                    }
                }
            }

        }
    }
}

pub fn pretty_print_tags(tags: &[Tag]) {
    if !tags.is_empty() {
        println!("|");
        println!("| // Tags //");

        let mut idx = 1;

        // Print tags with a standard tag key first, these are the most common tags.
        for tag in tags.iter().filter(| tag | tag.is_known()) {
            if let Some(std_key) = tag.std_key {
                println!("{}", pretty_print_tag_item(idx, &format!("{:?}", std_key), &tag.value, 4));
            }
            idx += 1;
        }

        // Print the remaining tags with keys truncated to 26 characters.
        for tag in tags.iter().filter(| tag | !tag.is_known()) {
            println!("{}", pretty_print_tag_item(idx, &tag.key, &tag.value, 4));
            idx += 1;
        }
    }
}

pub fn pretty_print_visuals(visuals: &[Visual]) {
    if !visuals.is_empty() {
        println!("|");
        println!("| // Visuals //");

        for (idx, visual) in visuals.iter().enumerate() {

            if let Some(usage) = visual.usage {
                println!("|     [{:0>2}] Usage:      {:?}", idx + 1, usage);
                println!("|          Media Type: {}", visual.media_type);
            }
            else {
                println!("|     [{:0>2}] Media Type: {}", idx + 1, visual.media_type);
            }
            if let Some(dimensions) = visual.dimensions {
                println!("|          Dimensions: {} px x {} px", dimensions.width, dimensions.height);
            }
            if let Some(bpp) = visual.bits_per_pixel {
                println!("|          Bits/Pixel: {}", bpp);
            }
            if let Some(ColorMode::Indexed(colors)) = visual.color_mode {
                println!("|          Palette:    {} colors", colors);
            }
            println!("|          Size:       {} bytes", visual.data.len());

            // Print out tags similar to how regular tags are printed.
            if !visual.tags.is_empty() {
                println!("|          Tags:");
            }

            for (tidx, tag) in visual.tags.iter().enumerate() {
                if let Some(std_key) = tag.std_key {
                    println!("{}", pretty_print_tag_item(tidx + 1, &format!("{:?}", std_key), &tag.value, 21));
                }
                else {
                    println!("{}", pretty_print_tag_item(tidx + 1, &tag.key, &tag.value, 21));
                }
            }
        }
    }
}

pub fn pretty_print_tag_item(idx: usize, key: &str, value: &Value, indent: usize) -> String {
    let key_str = match key.len() {
        0..=28 => format!("| {:w$}[{:0>2}] {:<28} : ", "", idx, key, w = indent),
        _ => format!("| {:w$}[{:0>2}] {:.<28} : ", "", idx, key.split_at(26).0, w = indent),
    };

    let line_prefix = format!("\n| {:w$} : ", "", w = indent + 4 + 28 + 1);
    let line_wrap_prefix = format!("\n| {:w$}   ", "", w = indent + 4 + 28 + 1);

    let mut out = String::new();

    out.push_str(&key_str);

    for (wrapped, line) in value.to_string().lines().enumerate() {
        if wrapped > 0 {
            out.push_str(&line_prefix);
        }

        let mut chars = line.chars();
        let split = (0..)
            .map(|_| chars.by_ref().take(72).collect::<String>())
            .take_while(|s| !s.is_empty())
            .collect::<Vec<_>>();

        out.push_str(&split.join(&line_wrap_prefix));
    }

    out
}
 */