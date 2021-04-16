use std::f32::consts::PI;


pub struct Sinewave {
    sample_rate: f32,
    frequency: f32
}

impl Sinewave {
    pub fn new(sample_rate: f32, frequency: f32) -> Sinewave {
        Sinewave { sample_rate, frequency }
    }

    pub fn make_sample(&self, index: usize) -> f32 {
        (2.0 * PI * self.frequency * (index as f32 / self.sample_rate)).sin()
    }
}