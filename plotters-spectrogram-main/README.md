# plotters-spectrogram
A proof of concept program that computes a spectrogram of a WAV file using:
* `hound` (APLv2) for parsing WAV files
* `ndarray` to store the numerical data (and make a few operations a bit more manageable)
* `rustFFT` to compute the FFT
* `plotters` (MIT) to plot the spectrogram, and
* `colorous` (APLv2) to give the spectrogram a decent color scheme

I'm intending to have this as a proof-of-concept for a larger program I'm writing, but this should be a great demonstration of how to compute spectrograms using the super-performant RustFFT library. For simplicity, I made the following compromises:
* Everything is single-threaded
* It's written like a script with a bunch of variables hard-coded and `.unwrap()` basically everywhere.

LICENSING:
I additionally wanted to avoid GPL licensing for this code (if you're fine with the GPL, just use `sonogram`; it's probably a lot easier). Libraries are licensed as follows:
* `hound`: APLv2
* `ndarray`: MIT/APLv2 Dual License
* `rustfft`: MIT/APLv2 Dual License
* `plotters`: MIT
* `colorous`: APLv2