async fn printOne() {
    for i in 0..10 {
        println!("One");
        sleep(Duration::from_millis(1000)).await;
    }
}

async fn printTwo() {
    for i in 0..5 {
        println!("Two");
        sleep(Duration::from_millis(1000)).await;
    }
}

#[tokio::main]
async fn main() {
    /*let mut v = Vec::new();
    for consumer in &self.consumers {
        v.push(consumer.consume());
    }
    join_all(v).await;*/

    let e = tokio::join!(printOne(), printTwo());
    println!("finished bitch");
}