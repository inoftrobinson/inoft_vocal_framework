use crate::base_transformer::BaseTransformer;
// use rustfft::{FftPlanner, num_complex::Complex};


struct Equalizer {

}

impl BaseTransformer<i16> for Equalizer {
    fn should_run(&mut self) -> bool {
        true
    }

    fn alter_sample(&mut self, sample_value: i16, sample_index: usize) -> i16 {
        /* let mut planner = FftPlanner::<f32>::new();
        let fft = planner.plan_fft_forward(1234);

        let mut buffer = vec![Complex{ re: 0.0, im: 0.0 }; 1234];

        fft.process(&mut buffer);
         */
        i16::MIN
    }
}