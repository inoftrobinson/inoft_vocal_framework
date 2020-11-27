#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

The soundfile module (https://PySoundFile.readthedocs.io/) has to be installed!

"""
"""import argparse
import os
import tempfile
import queue
import sys
import time

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def int_or_str(text):
    ""Helper function for argument parsing.""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()


def callback(indata, frames, time, status):
    ""This is called (from a separate thread) for each audio block.""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

class AudioRecording:
    def __init__(self):
        self.target_filepath = "/inoft_vocal_framework/platforms_handlers/c#/test.wav"
        # todo: add support for mp3
        self.samplerate = 44100
        self.num_channels = 2
        self.sound_file_subtype = "PCM_24"
        self.device_id = 1

    def start_recording(self):
        time_start = time.time()
        if args.samplerate is None:
            device_info = sd.query_devices(self.device_id, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        if args.filename is None:
            args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                            suffix='.wav', dir='')

        if os.path.exists(self.target_filepath):
            os.remove(self.target_filepath)

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(self.target_filepath, mode="x", samplerate=self.samplerate,
                          channels=self.num_channels, subtype=self.sound_file_subtype) as file:
            with sd.InputStream(samplerate=self.samplerate, device=self.device_id,
                                channels=self.num_channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
                    if time.time() > time_start + 10:
                        self.end_recording()

    def end_recording(self):
        print(f"\nRecording finished: {repr(args.filename)}")
        parser.exit(0)


if __name__ == "__main__":
    AudioRecording().start_recording()

# except Exception as e:
#    parser.exit(type(e).__name__ + ': ' + str(e))
"""