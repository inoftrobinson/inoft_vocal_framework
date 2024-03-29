use serde::Serialize;
use std::time::Instant;
use std::fs::File;

pub struct TraceItem {
    pub name: String,
    pub elapsed: u128,
    pub child: Option<Vec<TraceItem>>,
    start_instant: Instant
}

#[derive(Serialize)]
pub struct SerializedTraceItemData {
    pub n: String,  // name
    pub v: u128,  // value (elapsed)
    pub c: Option<Vec<SerializedTraceItemData>>  // child
}

impl TraceItem {
    pub fn new(name: String) -> TraceItem {
        TraceItem { name, elapsed: 0, child: None, start_instant: Instant::now() }
    }

    pub fn create_child(&mut self, name: String) -> &mut TraceItem {
        let child_item = TraceItem::new(name);
        let child_vec = self.child.get_or_insert(Vec::new());
        child_vec.push(child_item);
        child_vec.last_mut().unwrap()
    }

    pub fn close(&mut self) {
        self.elapsed = self.start_instant.elapsed().as_micros();
        println!("{} took {}s", self.name, self.elapsed as f32 / 1000000.0);
    }

    pub fn serialize(&self) -> SerializedTraceItemData {
        let serialized_child: Option<Vec<SerializedTraceItemData>>;
        if self.child.is_none() {
            serialized_child = None;
        } else {
            let mut active_child: Vec<SerializedTraceItemData> = Vec::new();
            for children in self.child.as_ref().unwrap() {
                active_child.push(children.serialize());
            }
            serialized_child = Some(active_child);
        }
        SerializedTraceItemData {
            n: self.name.clone(),
            v: self.elapsed,
            c: serialized_child
        }
    }

    pub fn to_string(&self) -> String {
        serde_json::to_string(&self.serialize()).unwrap()
    }

    pub fn to_file(&self, filepath: &str) {
        serde_json::to_writer(&File::create(filepath).unwrap(), &self.serialize()).unwrap();
    }
}

/*
struct Tracer {
    root_item: TraceItem
}

impl Tracer {
    pub fn new() -> Tracer {
        Tracer { root_item: TraceItem { name: root, value: 0, child: None } }
    }

    pub fn create_item(&mut self, name: String, value: usize) -> &TraceItem {
        let child_item = TraceItem { name, value, child: None };
        self.root_items.push(child_item);
        self.root_items.last().unwrap()
    }

    pub fn serialize(&self) {
        let e = self.root_items[0].serialize();
    }
}
 */