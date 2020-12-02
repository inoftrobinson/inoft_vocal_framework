fn main() {
    println!("cargo:rustc-env=OUT_DIR=C:/Users/LABOURDETTE/Desktop");
    println!("cargo:rustc-env=TARGET=x86_64-pc-windows-msvc");
    println!("cargo:rustc-env=OPT_LEVEL=0");
    println!("cargo:rustc-env=HOST=x86_64-pc-windows-msvc");
}