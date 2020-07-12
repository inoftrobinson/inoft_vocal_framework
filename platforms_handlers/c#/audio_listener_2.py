import sounddevice

duration = 10.5  # seconds
print("starting")
myrecording = sounddevice.rec(int(duration * 44100), samplerate=44100, channels=2)
sounddevice.wait()
print(myrecording)

