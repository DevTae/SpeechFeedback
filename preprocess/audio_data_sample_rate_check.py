import os
import librosa

path = "/workspace/kospeech/dataset/kspon/transcripts.txt"
target_sr = 16000

if os.path.isfile(path):
    with open(path, "r", encoding="utf8") as f:
        for line in f.readlines():
            path = line.split('\t')[0]
            sr = librosa.get_samplerate(path)
            if sr != target_sr:
                print(path, sr)
else:
    print("could not find the transcripts.txt")
