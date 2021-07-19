use serde::{Deserialize, Serialize};
use crate::models::EngineApiData;
use std::error::Error;
use reqwest::Url;
use bytes::Bytes;


#[derive(Debug, Serialize)]
struct Metadata {
    voiceKey: String,
}

#[derive(Debug, Serialize)]
struct SynthesiseGetDialogueRequestData {
    accessToken: String,
    text: String,
    metadata: Metadata,
}

#[derive(Debug, Deserialize)]
pub struct SynthesiseGetDialogueResponseData {
    pub success: bool,
    pub errorKey: Option<String>,
    pub protocol: Option<String>,
    pub bytes: Option<String>,
    pub url: Option<String>,
}


pub async fn synthesise_get_dialogue(
    engine_api_data: &EngineApiData, text: String, voice_key: String
) -> Result<Option<SynthesiseGetDialogueResponseData>, Box<dyn Error + Send + Sync>> {

    let client = reqwest::ClientBuilder::new().build().unwrap();
    let request_data = SynthesiseGetDialogueRequestData {
        text, metadata: Metadata { voiceKey: voice_key },
        accessToken: engine_api_data.access_token.clone()
            .expect("Specifying an access_token is required in order to synthesise dialogues with the Inoft Vocal Engine")
    };
    let request_jsonified_data = serde_json::to_string(&request_data).unwrap();

    let api_url = format!(
        "{}/api/v1/{}/{}/resources/synthesise-get-dialogue",
        engine_api_data.engine_base_url,
        engine_api_data.engine_account_id.as_ref()
            .expect("Specifying an engine_account_id is required in order to synthesise dialogues with the Inoft Vocal Engine"),
        engine_api_data.engine_project_id.as_ref()
            .expect("Specifying an engine_project_id is required in order to synthesise dialogues with the Inoft Vocal Engine")
    );
    let request = client
        .post(Url::parse(&*api_url).unwrap())
        .header("content-type", "application/json")
        .body(reqwest::Body::from(request_jsonified_data));

    match request.send().await {
        Ok(res) => {
            let response_text_content = res.text().await.unwrap();
            Ok(Some(serde_json::from_str(&*response_text_content).expect("Error in json")))
        },
        Err(err) => {
            println!("Error: {}", err);
            Ok(None)
        },
    }
}