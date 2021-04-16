use hound::WavSpec;


pub trait BaseTransformer {
    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16;
}