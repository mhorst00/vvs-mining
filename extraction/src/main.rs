use std::{env, fs};
use zstd;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("In file {}", file_path);
    let compressed_file = fs::read(file_path).expect("Unable to read file");
    println!("{}", compressed_file.len());

    let zsdt_decoder = zstd::Decoder::new(compressed_file);
}
