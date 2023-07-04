# Developed by DevTae@2023
# wav_timestamp_split.py 파일 실행 후에 진행하면 되는 스크립트 파일이다.
# 특정 음성 파일에 대한 다운 샘플링을 진행한다.
import os
import re
import librosa, soundfile

path = "/workspace/data"
files = os.listdir(path)

# 숫자로 끝나는, 즉, 타임프레임 기준으로 나눠진 파일들을 대상으로 함.
target_wav_files = [ filename for filename in files if re.match(r'^.*\d+\.wav', filename) ]
num_of_target_wav_files = len(target_wav_files)

# 일단, .wav -> _bak.wav 로 이름을 바꾼다. (만약, 이미 있다면 바꾸지 않음)
for idx, target_wav_file in enumerate(target_wav_files, start=1):
    old_file = os.path.join(path, target_wav_file)
    bak_file = old_file.replace(".wav", "_bak.wav")
    if not os.path.isfile(bak_file):
        os.rename(old_file, bak_file)
    print("renaming process :", idx / num_of_target_wav_files * 100, "% done.")

print("[done] renaming process is done.")


target_wav_files = [ filename for filename in files if filename.endswith("_bak.txt") ]
num_of_target_wav_files = len(target_wav_files)

orig_sr = 44100
target_sr = 16000

# 이름을 전부 바꾸었다면, 다운샘플링을 진행한다. 
for idx, target_wav_file in enumerate(target_wav_files, start=1):
    bak_file = os.path.join(path, target_wav_file)
    new_file = new_file.replace("_bak.wav", ".wav")
    if not os.path.isfile(new_file):
        y, _ = librosa.load(bak_file, sr=orig_sr)
        y_resample = librosa.resample(y, orig_sr=orig_sr, target_sr=target_sr)
        soundfile.write(new_file, y_resample, target_sr, format='wav')
    print("downsampling process :", idx / num_of_target_wav_files * 100, "% done.")

print("[done] downsampling process is done.")
