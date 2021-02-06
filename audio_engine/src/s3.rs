use rusoto_s3::{S3Client, PutObjectRequest, S3, CreateBucketRequest, DeleteBucketRequest, DeleteObjectRequest};
use rusoto_core::{Region, RusotoError};
use rusoto_core::credential::{AwsCredentials, DefaultCredentialsProvider, StaticProvider};
use std::fs::File;
use std::io::Read;
use std::env;
use tokio::time::sleep;

struct TestS3Client {
    region: Region,
    s3: S3Client,
    bucket_name: String,
    // This flag signifies whether this bucket was already deleted as part of a test
    bucket_deleted: bool,
}

impl TestS3Client {
    // construct S3 testing client
    fn new(bucket_name: String) -> TestS3Client {
        let region = if let Ok(endpoint) = env::var("S3_ENDPOINT") {
            let region = Region::Custom {
                name: "eu-west-3".to_owned(),
                endpoint: endpoint.to_owned(),
            };
            println!("picked up non-standard endpoint {:?} from S3_ENDPOINT env. variable", region);
            region
        } else {
            Region::UsEast1
        };

        TestS3Client {
            region: region.to_owned(),
            s3: S3Client::new(region),
            bucket_name: bucket_name.to_owned(),
            bucket_deleted: false,
        }
    }

    // construct an anonymous client for testing acls
    async fn create_anonymous_client(&self) -> S3Client {
        if cfg!(feature = "disable_minio_unsupported") {
            // Minio does not support setting acls, so to make tests pass, return a client that has
            // the credentials of the bucket owner.
            self.s3.clone()
        } else {
            S3Client::new_with(
                rusoto_core::request::HttpClient::new().expect("Failed to creat HTTP client"),
                StaticProvider::from(AwsCredentials::default()),
                self.region.clone(),
            )
        }
    }

    async fn create_test_bucket(&self, name: String) {
        let create_bucket_req = CreateBucketRequest {
            bucket: name.clone(),
            ..Default::default()
        };
        self.s3.create_bucket(create_bucket_req).await.expect("Failed to create test bucket");
        sleep(std::time::Duration::from_secs(5)).await;
    }

    async fn create_test_bucket_with_acl(&self, name: String, acl: Option<String>) {
        let create_bucket_req = CreateBucketRequest {
            bucket: name.clone(),
            acl,
            ..Default::default()
        };
        self.s3.create_bucket(create_bucket_req).await.expect("Failed to create test bucket");
    }

    async fn delete_object(&self, key: String) {
        let delete_object_req = DeleteObjectRequest {
            bucket: self.bucket_name.to_owned(),
            key: key.to_owned(),
            ..Default::default()
        };

        self.s3
            .delete_object(delete_object_req)
            .await
            .expect("Couldn't delete object");
    }

    async fn put_test_object(&self, filename: String) {
        let contents: Vec<u8> = Vec::new();
        let put_request = PutObjectRequest {
            bucket: self.bucket_name.to_owned(),
            key: filename.to_owned(),
            body: Some(contents.into()),
            ..Default::default()
        };

        self.s3
            .put_object(put_request)
            .await
            .expect("Failed to put test object");
    }

    async fn cleanup(&self) {
        if self.bucket_deleted {
            return;
        }

        let delete_bucket_req = DeleteBucketRequest {
            bucket: self.bucket_name.clone(),
            ..Default::default()
        };

        let s3 = self.s3.clone();
        let bucket_name = self.bucket_name.clone();

        match s3.delete_bucket(delete_bucket_req).await {
            Ok(_) => println!("Deleted S3 bucket: {}", bucket_name),
            Err(e) => println!("Failed to delete S3 bucket: {}", e),
        };
    }
}

async fn test_put_object_with_filename_and_acl(client: &S3Client, bucket: &str, dest_filename: &str, local_filename: &str, acl: Option<String>) {
    let mut f = File::open(local_filename).unwrap();
    let mut contents: Vec<u8> = Vec::new();
    match f.read_to_end(&mut contents) {
        Err(why) => panic!("Error opening file to send to S3: {}", why),
        Ok(_) => {
            let req = PutObjectRequest {
                bucket: bucket.to_owned(),
                key: dest_filename.to_owned(),
                body: Some(contents.into()),
                acl,
                ..Default::default()
            };
            let result = client.put_object(req).await.expect("Couldn't PUT object");
            println!("{:#?}", result);
        }
    }
}

pub async fn upload() {
    let bucket_name = "inoft-vocal-engine-web-test";
    let test_client = TestS3Client::new(String::from(bucket_name));

    // PUT an object via buffer (no_credentials is an arbitrary choice)
    test_put_object_with_filename_and_acl(
        &test_client.s3,
        &test_client.bucket_name,
        "out_from_rust.wav",
        &"F:/Sons utiles/text_optimized_wav_1.wav",
        Some("public-read".to_owned()),
    ).await;
}