use hound::WavReader;
use rustfft::{FftPlanner, num_complex::Complex};
use ndarray::{Array, Axis};
use plotters::prelude::*;
use ndarray_stats::QuantileExt;

const WINDOW_SIZE: usize = 1024;
const OVERLAP: f64 = 0.9;
const SKIP_SIZE: usize = (WINDOW_SIZE as f64 * (1f64 - OVERLAP)) as usize;

fn main() {
    let mut wav = WavReader::open("example.wav").unwrap();
    let samples = wav
        .samples()
        .collect::<Result<Vec<i16>, _>>()
        .unwrap();
    
    println!("Creating windows {window_size} samples long from a timeline {num_samples} samples long, picking every {skip_size} windows with a {overlap} overlap for a total of {num_windows} windows.",
        window_size = WINDOW_SIZE, num_samples = samples.len(), skip_size = SKIP_SIZE, overlap = OVERLAP, num_windows = (samples.len() / SKIP_SIZE) - 1,
    );

    // Convert to an ndarray
    // Hopefully this will keep me from messing up the dimensions
    // Mutable because the FFT takes mutable slices &[Complex<f32>]
    // let window_array = Array2::from_shape_vec((WINDOW_SIZE, windows_vec.len()), windows_vec).unwrap();

    let samples_array = Array::from(samples.clone());
    let windows = samples_array
        .windows(ndarray::Dim(WINDOW_SIZE))
        .into_iter()
        .step_by(SKIP_SIZE)
        .collect::<Vec<_>>()
        ;
    let windows = ndarray::stack(Axis(0), &windows).unwrap();

    // So to perform the FFT on each window we need a Complex<f32>, and right now we have i16s, so first let's convert
    let mut windows = windows.map(|i| Complex::from(*i as f32));


    // get the FFT up and running
    let mut planner = FftPlanner::new();
    let fft = planner.plan_fft_forward(WINDOW_SIZE);

    // Since we have a 2-D array of our windows with shape [WINDOW_SIZE, (num_samples / WINDOW_SIZE) - 1], we can run an FFT on every row.
    // Next step is to do something multithreaded with Rayon, but we're not cool enough for that yet.
    windows.axis_iter_mut(Axis(0))
        .for_each(|mut frame| { fft.process(frame.as_slice_mut().unwrap()); });
    
    // Get the real component of those complex numbers we get back from the FFT
    let windows = windows.map(|i| i.re);

    // And finally, only look at the first half of the spectrogram - the first (n/2)+1 points of each FFT
    // https://dsp.stackexchange.com/questions/4825/why-is-the-fft-mirrored
    let windows = windows.slice_move(ndarray::s![.., ..((WINDOW_SIZE / 2) + 1)]);

    // get some dimensions for drawing
    // The shape is in [nrows, ncols], but we want to transpose this.
    let (width, height) = match windows.shape() {
        &[first, second] => (first, second),
        _ => panic!("Windows is a {}D array, expected a 2D array", windows.ndim())
    };
    

    println!("Generating a {} wide x {} high image", width, height);

    let image_dimensions: (u32, u32) = (width as u32, height as u32);
    let root_drawing_area = 
        BitMapBackend::new(
            "output.png", 
            image_dimensions, // width x height. Worth it if we ever want to resize the graph.
        ).into_drawing_area();

    let spectrogram_cells = root_drawing_area.split_evenly((height, width));

    let windows_scaled = windows.map(|i| i.abs()/(WINDOW_SIZE as f32));
    let highest_spectral_density = windows_scaled.max_skipnan();
    
    // transpose and flip around to prepare for graphing
    /* the array is currently oriented like this:
        t = 0 |
              |
              |
              |
              |
        t = n +-------------------
            f = 0              f = m

        so it needs to be flipped...
        t = 0 |
              |
              |
              |
              |
        t = n +-------------------
            f = m              f = 0

        ...and transposed...
        f = m |
              |
              |
              |
              |
        f = 0 +-------------------
            t = 0              t = n
        
        ... in order to look like a proper spectrogram
    */
    let windows_flipped = windows_scaled.slice(ndarray::s![.., ..; -1]); // flips the
    let windows_flipped = windows_flipped.t();

    // Finally add a color scale
    let color_scale = colorous::MAGMA;

    for (cell, spectral_density) in spectrogram_cells.iter().zip(windows_flipped.iter()) {
            let spectral_density_scaled = spectral_density.sqrt() / highest_spectral_density.sqrt();
            let color = color_scale.eval_continuous(spectral_density_scaled as f64);
            cell.fill(&RGBColor(color.r, color.g, color.b)).unwrap();
        };
}
