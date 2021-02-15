fn main() {
    println!("yol");
    build::main();
}

/*#[cfg(not(feature = "bundled"))]
mod build {
    use std::env;

    pub fn main() {
        println!("nooon");
        if let Ok(dir) = env::var("LAME_LIB_DIR") {
            println!("cargo:rustc-link-search=native={}", dir);
        }

        if env::var("LAME_STATIC").is_ok() {
            println!("cargo:rustc-link-lib=static=mp3lame");
        } else {
            println!("cargo:rustc-link-lib=dylib=mp3lame");
        }
    }
}

 */

// #[cfg(feature = "bundled")]
mod build {
    extern crate gcc;

    use std::env;

    pub fn main() {
        println!("ninka");

        let target_os = env::var("CARGO_CFG_TARGET_OS").unwrap_or(String::from("windows"));  // .expect("CARGO_CFG_TARGET_OS not set");
        let target_arch = env::var("CARGO_CFG_TARGET_ARCH").unwrap_or(String::from("x86"));  // .expect("CARGO_CFG_TARGET_ARCH not set");

        let mut config = gcc::Config::new();

        config
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/bitstream.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/encoder.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/fft.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/gain_analysis.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/id3tag.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/lame.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/mpglib_interface.c") //Perhaps remove
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/newmdct.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/presets.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/psymodel.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/quantize_pvt.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/quantize.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/reservoir.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/set_get.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/tables.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/takehiro.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/util.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/vbrquantize.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/VbrTag.c")
            .file("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame/version.c")
            .include("C:/Users/LABOURDETTE/Desktop/lame-3.100/include")
            .include("C:/Users/LABOURDETTE/Desktop/lame-3.100/libmp3lame")
            .define("HAVE_CONFIG_H", None)
            .define("PIC", None);

        if target_os == "windows" {
            config
                .define("TAKEHIRO_IEEE754_HACK", None)
                .define("FLOAT8", Some("float"))
                .define("REAL_IS_FLOAT", Some("1"))
                .define("BS_FORMAT", Some("BINARY"));
        }

        let os_config_dir = match &*target_os {
            "linux" => "linux",
            "macos" => "mac",
            "windows" => "win",
            os => panic!("unsupported os {}", os),
        };

        let arch_config_dir = match &*target_arch {
            "x86" => "ia32",
            "x86_64" => "x64",
            "arm" => "arm",
            arch => panic!("unsupported arch {}", arch),
        };

        println!("start...");

        config.include(format!("lame-config/{}/{}", os_config_dir, arch_config_dir));

        config.compile("C:/Users/LABOURDETTE/Desktop/libmp3lame.a");
        println!("finished...");
    }
}
