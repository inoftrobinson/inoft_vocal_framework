// #![allow(dead_code)]
// #![allow(unused_imports)]
// #![allow(unused_variables)]

mod append;
mod resampler;
// mod renderer;
mod exporter;
// mod s3;
#[path="models.rs"] pub mod models;
#[path="renderer.rs"] pub mod renderer;
#[path="loader.rs"] pub mod loader;
#[path="hasher.rs"] pub mod hasher;
#[path="tests/mod.rs"] pub mod tests;
use models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, Time};
mod audio_clip;
use audio_clip::AudioClip;


mod lib;

use std::f32::consts::PI;
use std::{i16, thread};
use hound;
use hound::{WavReader, WavSamples};
use std::io::BufReader;
use std::fs::File;
use std::ptr::null;
use tokio;
use tokio::prelude::*;
// use tokio::time::error::Error;
use reqwest;
use tokio::net::{TcpStream, TcpListener};
use std::sync::mpsc;
use std::future::Future;
use std::net::IpAddr;


fn main() {
    println!("No");
}