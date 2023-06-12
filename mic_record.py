import sounddevice as sd
from scipy.io.wavfile import write

# the duration of the recording in seconds
duration = 5.0

# the sample rate (in samples/sec), change this value if needed
sample_rate = 44100

# use the sounddevice library to record audio
print("Starting recording...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  # wait until the recording is done
print("Recording finished.")

# use the scipy library to save the numpy array into a .wav file
write("output.wav", sample_rate, recording)

#### 이따가 확인