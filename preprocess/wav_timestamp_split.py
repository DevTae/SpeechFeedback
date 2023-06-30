# Developed by DevTae@2023
# 극한소음 데이터셋에서 정해진 타임스탬프에 대하여 분할 저장해주는 스크립트

import os
import json
import librosa
import soundfile

root_path = "/workspace/data"
file_list = os.listdir(root_path)
file_list_json = [file for file in file_list if file.endswith(".json")]
total_num = len(file_list_json)

for num, json_path in enumerate(file_list_json):
    try:
        json_file = open(os.path.join(root_path, json_path), "r")
        json_data = json.loads(json_file.read())

        wav_path_VN = json_data.get("mediaUrl").split('/')[-1]
        wav_path_VN = os.path.join(root_path, wav_path_VN)
        wav_path_NV = wav_path_VN.replace("VN", "NV")
        
        if wav_path_VN == wav_path_NV:
            continue
        
        dialogs = json_data.get("dialogs")
        
        wav_data_VN, sr = librosa.load(path=wav_path_VN, sr=44100)
        wav_data_NV, sr = librosa.load(path=wav_path_NV, sr=44100)
        
        for idx, dialog in enumerate(dialogs):
            # load the attributes
            speakerText = dialog["speakerText"]
            startTime = float(dialog["startTime"])
            endTime = float(dialog["endTime"])

            # split VN audio file and save the transcript
            wav_path_VN_splited = wav_path_VN.replace(".wav", "_" + str(idx) + ".wav")
            wav_data_VN_splited = wav_data_VN[int(sr*startTime):int(sr*endTime)]
            soundfile.write(wav_path_VN_splited, wav_data_VN_splited, sr, format='wav')
            txt_data_VN_splited = open(wav_path_VN_splited.replace(".wav", ".txt"), "w")
            txt_data_VN_splited.write(speakerText)
            txt_data_VN_splited.close()

            # split NV audio file and save the transcript
            wav_path_NV_splited = wav_path_NV.replace(".wav", "_" + str(idx) + ".wav")
            wav_data_NV_splited = wav_data_NV[int(sr*startTime):int(sr*endTime)]
            soundfile.write(wav_path_NV_splited, wav_data_NV_splited, sr, format='wav')
            txt_data_NV_splited = open(wav_path_NV_splited.replace(".wav", ".txt"), "w")
            txt_data_NV_splited.write(speakerText)
            txt_data_NV_splited.close()

    except:
        continue

    print(str(num / total_num) + "% done")

