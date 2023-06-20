# Copyright (c) 2020, Soohwan Kim. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import librosa

import sys
import ipa_converter # 만약 ipa_converter 이용 시, /workspace/kospeech/dataset/kspon 폴더에 csv/* 와 ipa_converter.py 를 옮겨야 한다.

def bracket_filter(sentence, mode='phonetic'):
    new_sentence = str()

    if mode == 'phonetic':
        flag = False

        for ch in sentence:
            if ch == '(' and flag is False:
                flag = True
                continue
            if ch == '(' and flag is True:
                flag = False
                continue
            if ch != ')' and flag is False:
                new_sentence += ch

    elif mode == 'spelling':
        flag = True

        for ch in sentence:
            if ch == '(':
                continue
            if ch == ')':
                if flag is True:
                    flag = False
                    continue
                else:
                    flag = True
                    continue
            if ch != ')' and flag is True:
                new_sentence += ch

    else:
        raise ValueError("Unsupported mode : {0}".format(mode))

    return new_sentence


def special_filter(sentence, mode='phonetic', replace=None):
    new_sentence = str()
    for idx, ch in enumerate(sentence.replace("\n", " ")):
        if re.search(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ ]", ch) is None:
            continue
        new_sentence += ch

    pattern = re.compile(r'\s\s+') # 스페이스바 두 번 이상일 때
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence


def sentence_filter(raw_sentence, mode, replace=None):
    return special_filter(bracket_filter(raw_sentence, mode), mode, replace)


def preprocess(dataset_path, mode='phonetic'):
    print('preprocess started..')

    audio_paths = list()
    transcripts = list()

    BASE_PATH = dataset_path
    META_PATH = "/전시문_통합_스크립트/KsponSpeech_scripts/train.trn"
    path = BASE_PATH + META_PATH

    if not os.path.isfile(path):
        raise Exception("[error] the metadata file is not found.")

    with open(path, "r", encoding='utf8') as f:
        for j, line in enumerate(f.readlines(), start=1):
            datas = line.split(' :: ')
            audio_path = BASE_PATH + "/한국어_음성_분야/" + datas[0].strip()
            sentence = str()
            try:
                with open(audio_path.replace(".pcm", ".txt"), "r", encoding="cp949") as sentence_f: # utf8 -> cp949 (한국어 음성 데이터셋)
                    sentence = sentence_filter(sentence_f.read(), mode=mode)
                if sentence is None:
                    continue

                # 라벨링 데이터 대비 음성 길이 비율을 바탕으로 필터링 진행
                # 한 번 필터 없이 돌린 이후 audio_data_audio_length.py 바탕으로 판단 후 적용
                #audio_duration = librosa.get_duration(librosa.load(audio_path, sr=16000)[0], sr=16000)
                #transcript_length = len(sentence)
                #ratio = audio_duration / transcript_length
                #if ratio > 0.2316 or ratio < 0.1047:
                #    continue

                audio_paths.append(audio_path)
                #transcripts.append(sentence)
                transcripts.append(ipa_converter.applyRulesToHangulTotal(sentence)) # ipa_convert 이용 시 위 코드 주석한 후 해당 코드 주석 해제

            except:
                print(audio_path)
                continue

    return audio_paths, transcripts
