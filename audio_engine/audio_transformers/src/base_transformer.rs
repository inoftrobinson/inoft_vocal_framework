use hound::WavSpec;


pub trait BaseTransformer<T> {
    fn should_run(&mut self) -> bool;

    fn alter_sample(&mut self, sample_value: T, sample_index: usize) -> T;
}