use tokio::time::{Duration, sleep};

/*
fn write_sinewave(filepath: &str) {
    let spec = hound::WavSpec {
        channels: 1,
        sample_rate: 44100,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };
    let mut writer = hound::WavWriter::create(filepath, spec).unwrap();
    for t in (0 .. 44100).map(|x| x as f32 / 44100.0) {
        let sample = (t * 440.0 * 2.0 * PI).sin();
        let amplitude = i16::MAX as f32;
        writer.write_sample((sample * amplitude) as i16).unwrap();
    }
}
 */


/*
fn open_wav_file(filepath: &str) -> WavReader<BufReader<File>> {
    let mut reader = WavReader::open(filepath).unwrap();
    reader

    /*println!("Opened");
    let v = reader.samples::<i16>();
    v*/
    // &v
}
 */

/*
fn square(mut reader: WavReader<BufReader<File>>) {
    println!("Opened");
    let sqr_sum = reader.samples::<i16>().fold(0.0, |sqr_sum, s| {
        let sample = s.unwrap() as f64;
        // println!("{}", sample);
        sqr_sum + sample * sample;
        sqr_sum
    });
    println!("RMS is {}", (sqr_sum / reader.len() as f64).sqrt());
}
 */

/*
fn change_volume(mut reader: WavReader<BufReader<File>>) {
    let sqr_sum = reader.samples::<i16>().for_each(0.0, |sqr_sum, s| {
        let sample = s.unwrap() as f64;
        println!("{}", sample);
        sqr_sum + sample * sample;
        sqr_sum
    });
    println!("RMS is {}", (sqr_sum / reader.len() as f64).sqrt());
}
 */

/*async fn upload() {
    let e = s3::upload().await;
}*/

/*
fn main() {
    let ip_addr = "172.217.3.238".parse::<IpAddr>().unwrap();

    // Improved Simplified Solution
    println!("[Simple] Reverse Ip Look Results For: {}", ip_addr);
    let handle = create_simple_lookup_handle();
    let result_future = handle.lookup_hostnames(ip_addr);
    for hostname in result_future.wait().unwrap() {
        println!(" - {}", hostname);
    }
}

async fn write_data() {
    // let mut stream = TcpStream::connect("127.0.0.1:8000").await.unwrap();
    // stream.write_all(b"test").await.unwrap();
    let prom = tokio::time::sleep(Duration::from_millis(3000)).await;
    println!("yolo");
}

async fn log() {
    println!("goodday");
}
 */

/*#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;

    loop {
        let (mut socket, _) = listener.accept().await?;

        tokio::spawn(async move {
            let mut buf = [0; 1024];

            // In a loop, read data from the socket and write the data back.
            loop {
                println!("Reading...");
                let n = match socket.read(&mut buf).await {
                    // socket closed
                    Ok(n) if n == 0 => return,
                    Ok(n) => n,
                    Err(e) => {
                        eprintln!("failed to read from socket; err = {:?}", e);
                        return;
                    }
                };

                // Write the data back
                if let Err(e) = socket.write_all(&buf[0..n]).await {
                    eprintln!("failed to write to socket; err = {:?}", e);
                    return;
                }
            }
        });
    }
}
 */

/*
#[tokio::main]
async fn main() {
    write_data().await;
    log().await;
    /*let res = reqwest::get("http://httpbin.org/get").await;
    println!("Status: {}", res.status());
    println!("Headers:\n{:#?}", res.headers());

    let body = res.unwrap().text().await;
    println!("Body:\n{}", body.unwrap());
    Ok(())

     */
}
 */

/*

use mini_redis::{client, Result};

#[tokio::main]
pub async fn main() -> Result<()> {
    let handle = tokio::spawn(async {
        let prom = tokio::time::sleep(Duration::from_millis(3000)).await;
        println!("yolo");
    });

    let out1 = tokio::spawn(async {
        println!("my dude !");
    }).await;

    // Do some other work

    let out2 = handle.await.unwrap();
    println!("GOT {:?}", out2);

    let out3 = tokio::spawn(async {
        println!("whuuuttt !");
    }).await;


    // Open a connection to the mini-redis address.
    let mut client = client::connect("127.0.0.1:6379").await?;

    // Set the key "hello" with value "world"
    client.set("hello", "world".into()).await?;

    // Get key "hello"
    let result = client.get("hello").await?;

    println!("got value from the server; result={:?}", result);

    Ok(())
}

fn create_simple_lookup_handle() -> SimpleDnsLookupHandle {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        let mut core = Core::new().unwrap();
        let resolv = Resolver::new(&core.handle());
        tx.send(resolv);
        loop { core.turn(None); }
    });

    return SimpleDnsLookupHandle { resolv: rx.recv().unwrap() }
}


#[derive(Clone)]
pub struct SimpleDnsLookupHandle {
    resolv: Resolver,
}

impl SimpleDnsLookupHandle {
    pub fn lookup_hostnames(&self, ip: IpAddr) -> impl Future<Item=Vec<String>, Error=()> {
        lookup_addr(self.resolv.clone(), ip).map_err(|e| println!("error = {:?}", e))
                                    .map(|addrs| addrs.iter().map(|n| n.to_string()).collect())
    }
}
 */

/*
fn main() {
    let mut rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        println!("hello");
    });
    rt.block_on(async {
        let req = Request::builder()
            .method(Method::POST)
            .uri("http://127.0.0.1:5000/api/v1/@robinsonlabourdette/livetiktok/resources/project-audio-files/generate-presigned-upload-url")
            .header("content-type", "application/json")
            .body(Body::from(""));

        let client = Client::new();
        let resp = client.request(req.unwrap()).await;
        println!("Response: {:?}", resp);
        resp
    });

    // append::main();
    // let res = exporter::from_flac_to_mp3().await;
    /*

    let arr: [u32; 5] = [1, 2, 3, 4, 5];
    for item in arr.iter() {
        println!("{}", item);
    }

    write_sinewave("F:/Sons utiles/sine.wav");
    change_volume(WavReader::open("F:/Sons utiles/test1.wav").unwrap());
     */
}
 */