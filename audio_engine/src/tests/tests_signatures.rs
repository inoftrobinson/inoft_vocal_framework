#[cfg(test)]
mod tests_signature {
    use crate::tests::samples;
    use crate::hasher;
    use std::thread::sleep;

    #[test]
    fn hash() {
        let mut data = samples::make_sample_project_data();
        let initial_signature = hasher::hash(&data);

        data.blocks[0].tracks[0].clips.reverse();
        let signature_with_reversed_clips = hasher::hash(&data);

        assert_eq!(initial_signature, signature_with_reversed_clips);
        println!("Finished hashing...");
    }
}