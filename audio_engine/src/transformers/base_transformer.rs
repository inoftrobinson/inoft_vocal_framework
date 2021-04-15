use hound::WavSpec;


pub trait BaseTransformer {
    fn new(parent_renderer_target_wav_spec: &WavSpec) -> Self;

    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16;
}