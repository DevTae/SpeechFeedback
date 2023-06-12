import librosa, soundfile

path = "/workspace/data/test/1.wav" # what wav file you want to convert
target_sr = 16000 # what rate you want to resample

y, sr = librosa.load(path, sr=librosa.get_samplerate(path))
y_resample = librosa.resample(y, orig_sr=sr, target_sr=target_sr) # target_sr is 16000

soundfile.write(path.replace(".wav", "_converted.wav"), y_resample, target_sr, format='wav')
