"""
The Python TraceItem directly tries to mimic the api of the Rust TraceItem, found at ./audio_engine/src/tracer.rs
"""


import time
from typing import Optional, List


class TraceItem:
    def __init__(self, name: str, children: Optional[list] = None):
        self.name = name
        self.children: List[TraceItem or dict] = children or []
        self.start_instant = int(time.time() * 1000000)
        self.elapsed: Optional[int] = None

    def add_child(self, child_item: dict):
        self.children.append(child_item)

    def create_child(self, name: str, children: Optional[list] = None):
        child_item = TraceItem(name=name, children=children)
        self.children.append(child_item)
        return child_item

    def close(self):
        self.elapsed = int(time.time() * 1000000) - self.start_instant
        print(f"{self.name} took {self.elapsed / 1000000}s")

    def serialize(self):
        serialized_children: List[dict] = [
            child.serialize() if isinstance(child, TraceItem) else child
            for child in self.children
        ]
        return {
            'n': self.name,
            'v': self.elapsed,
            'c': serialized_children
        }
