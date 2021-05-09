#[cfg(test)]
mod tests_exports {
    use crate::{append, exporter};
    use crate::models::{ReceivedParsedData, ReceivedTargetSpec, AudioBlock, Track, AudioClip, Time};
    use std::cell::RefCell;
    use tokio;
    use tokio::prelude::*;
    use std::collections::HashMap;
    use reqwest::Url;
    // use crate::hound2;
    use hound::WavReader;
    use std::io::{BufReader, Read};
    use tokio::fs;
    use std;
    use std::time::Instant;
    use crate::loader::{get_file_bytes_from_url};
    use crate::tests::samples;

    async fn resample() {
        let data = samples::make_sample_project_data();
        /*let task_1 = tokio::spawn(exporter::get_upload_url(String::from("test.mp3"), 1000));
        let task_2 = tokio::spawn(append::main(data));
        let tasks = tokio::join!(task_1, task_2);*/
        // let mut runtime = tokio::runtime::Runtime::new().unwrap();
        // let file_url = runtime.block_on(append::main(parsed_data));
        println!("Finished tokio...");
    }

    #[test]
    fn resample_test() {
        let mut runtime = tokio::runtime::Runtime::new().unwrap();
        runtime.block_on(resample());
    }

    async fn get_file_from_url() {
        let url = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/output_final.wav";
        let bytes = get_file_bytes_from_url(url).await;
        let wave_reader = WavReader::new(BufReader::new(&*bytes)).unwrap();
    }

    #[test]
    fn get_file_from_url_test() {
        let mut runtime = tokio::runtime::Runtime::new().unwrap();
        runtime.block_on(get_file_from_url());
    }
}