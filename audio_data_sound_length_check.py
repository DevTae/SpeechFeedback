# Developed by DevTae@2023
# For classifying and analyzing the audio datas, checking the data's duration per second is needed.

import librosa
import numpy as np

path = "/workspace/kospeech/dataset/kspon/transcripts.txt"

with open(path, "r", encoding="utf8") as r:
  audio_paths = []
  audio_durations = []
  transcript_lengths = []
  ratios = []
  for line in r.readlines():
    try:
      audio_path, transcript, _ = line.split('\t');
      audio_paths.append(audio_path)
      audio_duration = librosa.get_duration(librosa.load(audio_path, sr=16000)[0], sr=16000)
      audio_durations.append(audio_duration)
      transcript_length = len(transcript)
      transcript_lengths.append(transcript_length)
      ratio = audio_duration / transcript_length
      ratios.append(ratio)
      print("ratio :", ratio)
    except:
      continue
      
  print("max is", max(ratio)) # max is 23.21
  print("min is", min(ratio)) # min is 0.0
  print("avg is", sum(ratio)/len(ratio)) # 0.1628 ...
  print("np.percentile is")
  print(np.percentile(ratio, q=[0, 25, 50, 75, 100]))
  # np.percentile is
  # [ 0.0000 0.1047 0.1156 0.1242 0.1333
  #   0.1431 0.1550 0.1707 0.2316 23.21 ]
