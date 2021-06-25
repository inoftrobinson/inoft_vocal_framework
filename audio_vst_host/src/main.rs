// mod window;

#[macro_use]
extern crate vst;
extern crate libc;

#[cfg(windows)]
#[macro_use]
extern crate memoffset;
#[cfg(windows)]
#[macro_use]
extern crate winapi;

mod windows_opengl_vst;

use std::env;
use std::path::Path;
use std::process;
use std::sync::{Arc, Mutex};

use vst::host::{Host, PluginLoader};
use vst::plugin::Plugin;
use winapi::HWND__;

use hound::{WavReader, WavSpec};
use vst::buffer::AudioBuffer;
use std::convert::TryFrom;
use std::borrow::BorrowMut;

use beryllium::*;
use gl33::*;
use ogl33::c_void;
use std::any::Any;
use std::ops::Deref;


#[allow(dead_code)]
struct SampleHost;

impl Host for SampleHost {
    fn automate(&self, index: i32, value: f32) {
        println!("Parameter {} had its value changed to {}", index, value);
    }
}

fn main() {
    let sdl = SDL::init(InitFlags::Everything).expect("couldn't start SDL");
    sdl.gl_set_attribute(SdlGlAttr::MajorVersion, 3).unwrap();
    sdl.gl_set_attribute(SdlGlAttr::MinorVersion, 3).unwrap();
    sdl.gl_set_attribute(SdlGlAttr::Profile, GlProfile::Core).unwrap();

    let _win = sdl
        .create_gl_window(
            "Sample window",
            WindowPosition::Centered,
            800,
            600,
            WindowFlags::Shown,
        )
        .expect("couldn't make a window and context");

    /*let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("usage: simple_host path/to/vst");
        process::exit(1);
    }*/

    // let st_path = "C:/Users/LABOURDETTE/Downloads/DragonflyReverb-Windows-64bit-v3.2.5/DragonflyReverb-Windows-64bit-v3.2.5/DragonflyEarlyReflections-vst.dll";
    let st_path = "C:/Program Files/Steinberg/VSTPlugins/Brusfri.dll";
    let path = Path::new(st_path);  // &args[1]);

    // Create the host
    let host = Arc::new(Mutex::new(SampleHost));

    println!("Loading {}...", path.to_str().unwrap());

    // Load the plugin
    let mut loader = PluginLoader::load(path, Arc::clone(&host))
        .unwrap_or_else(|e| panic!("Failed to load plugin: {}", e));

    // Create an instance of the plugin
    let mut instance = loader.instance().unwrap();

    // Get the plugin information
    let info = instance.get_info();

    println!(
        "Loaded '{}':\n\t\
         Vendor: {}\n\t\
         Presets: {}\n\t\
         Parameters: {}\n\t\
         VST ID: {}\n\t\
         Version: {}\n\t\
         Initial Delay: {} samples",
        info.name, info.vendor, info.presets, info.parameters, info.unique_id, info.version, info.initial_delay
    );

    // Initialize the instance
    instance.init();
    println!("Initialized instance!");

    let preset_name = instance.get_parameter_object().get_preset_name(0);
    println!("preset : {}", preset_name);

    // instance.get_parameter_object().
    instance.get_parameter_object().set_parameter(0, 100.0);
    instance.get_parameter_object().set_parameter(1, 100.0);
    instance.get_parameter_object().string_to_parameter(2, 2.0.to_string());
    instance.get_parameter_object().set_parameter(3, 60.0);
    instance.get_parameter_object().set_parameter(4, 100.0);
    instance.get_parameter_object().set_parameter(5, 60.0);
    instance.get_parameter_object().set_parameter(6, 5000.0);
    // instance.get_parameter_object().set_preset_name(preset_name);
    for idx in 0..info.parameters {
        println!("{}", instance.get_parameter_object().get_parameter_name(idx));
        println!("{}", instance.get_parameter_object().get_parameter(idx));
        // instance.get_parameter_object().set_parameter(idx, 100.0);
    }

    // let window = windows_opengl_vst::

    let win_ref: &GlWindow = &_win;
    // win_ref.get_proc_address(b"window");
    /*if my_num_ptr.is_null() {
        panic!("failed to allocate memory");
    }*/
    // let win_pointer = win_ref as *mut libc::c_void;
    // libc::free(my_num as *mut libc::c_void);

    let mut bar: *mut GlWindow = std::ptr::null_mut();
    // let mut_ref: &mut *mut GlWindow = &mut bar;
    /*let raw_ptr: *mut *mut foo = mut_ref as *mut *mut _;
    let void_cast: *mut *mut c_void = raw_ptr as *mut *mut c_void;*/
    let raw_ptr: *mut GlWindow = bar as *mut _;
    let void_cast: *mut c_void = raw_ptr as *mut c_void;
    // unsafe { ffi(void_cast); }

    instance.get_editor().unwrap().open(void_cast);

    let mut buffer = hound::WavReader::open("../samples/audio/hop_short_wav_16bit.wav").unwrap();
    // let samples = buffer.samples();
    // let mut audio_buffer: AudioBuffer<f64> = AudioBuffer::try_from(buffer.samples().buffer()).unwrap();

    let mut out1 = vec![0.0; buffer.duration() as usize];
    let mut out2 = out1.clone();
    let mut outputs = vec![out1.as_mut_ptr(), out2.as_mut_ptr()];

    let samples: Vec<i32> = buffer
        .samples()
        .collect::<Result<Vec<i32>, _>>()
        .unwrap();
    let mut samples: Vec<f32> = samples.iter()
        .map(|s| s.clone() as f32)
        .collect::<Vec<f32>>();

    /*let mut in1 = vec![0.0; buffer.duration() as usize];
    let mut in2 = in1.clone();
    let mut inputs = vec![in1.as_ptr(), in2.as_ptr()];*/
    let rar = samples.clone();
    let rar2 = rar.clone();
    let inputs = vec![rar.as_ptr(), rar2.as_ptr()];

    println!("Before creating buffer");

    // let samples: Vec<f64> = buffer.samples().map(|s| s.unwrap()).collect();
    let channels = buffer.spec().channels as usize;
    let inputs_rar = inputs.as_ptr();
    let outputs_mut_ptr = outputs.as_mut_ptr();
    let duration = buffer.duration() as usize;

    let mut audio_buffer = unsafe {
        AudioBuffer::from_raw(
            channels,
            channels,
            inputs_rar,
            outputs_mut_ptr,
            duration
        )
    };
    println!("Buffer created");
    instance.process(audio_buffer.borrow_mut());

    let split = audio_buffer.split();
    let channel = split.1.get(0);
    let channel2 = split.1.get(1);
    let mut finale = channel.to_vec();
    finale.append(&mut channel2.to_vec());
    write_wav_samples_to_file(
        // audio_buffer.zip().map(|s| s.1).collect::<Vec<f32>>(), buffer.spec(),
        // channel.to_vec(), buffer.spec(),
        finale, buffer.spec(),
        "F:/Inoft/anvers_1944_project/inoft_vocal_framework/dist/vst_support/output1.wav"
    );


    // let window = window::Win32Window::new()
    // instance.get_editor().unwrap().open(winapi::HWND__);

    println!("Closing instance...");
    // Close the instance. This is not necessary as the instance is shut down when
    // it is dropped as it goes out of scope.
    // drop(instance);

    // vst_gui_rs::synth::main(_win);

    'main_loop: loop {
        // handle events this frame
        while let Some(event) = sdl.poll_events().and_then(Result::ok) {
          match event {
            Event::Quit(_) => break 'main_loop,
            _ => (),
          }
        }
        // now the events are clear

        // here's where we could change the world state and draw.
      }
    println!("ended things");
}

unsafe fn rar(mut win: GlWindow) {

}

pub fn write_wav_samples_to_file(wav_samples: Vec<f32>, wav_target_spec: WavSpec, filepath: &str) -> Result<String, Box<hound::Error>> {
    match hound::WavWriter::create(filepath, wav_target_spec) {
        Ok(mut writer) => {
            for sample in wav_samples {
                writer.write_sample(sample as i16).unwrap();
            }
            Ok(String::from(filepath))
        },
        Err(err) => {
            println!("Wav writer error : {}", err);
            Err(Box::new(err))
        }
    }
}