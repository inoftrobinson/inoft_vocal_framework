use crate::{AudioBlock};


pub struct ReceivedTargetSpec {
    pub sample_rate: i32,
}

pub struct ReceivedParsedData {
    pub blocks: Vec<AudioBlock>,
    pub target_spec: ReceivedTargetSpec,
}
