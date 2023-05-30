# Developed by DevTae@2023
# For classifying and analyzing the audio datas, checking the data's duration per second is needed.

import librosa

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
    catch:
      continue
      
  print("max is", max(ratio))
  print("min is", min(ratio))
  print("avg is", sum(ratio)/len(ratio))
  print("np.percentile is")
  print(np.percentile(ratio, q=[0, 25, 50, 75, 100]))
