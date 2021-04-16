use hound::WavSpec;


pub trait BaseTransformer {
    fn alter_sample(&mut self, sample_value: f32, sample_index: usize) -> f32;
}