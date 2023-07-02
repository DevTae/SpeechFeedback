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
#import ipa_converter # 만약 ipa_converter 이용 시, /workspace/kospeech/dataset/kspon 폴더에 csv/* 와 ipa_converter.py 를 옮겨야 한다.
import eng_to_ipa as ipa # Install the mphilli/English-to-IPA library

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
    for idx, ch in enumerate(sentence.replace("\n", " ").lower()):
        if re.search(r"[a-z ]", ch) is None:
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
    TYPE_PATH = "train"
    META_PATH = os.path.join(BASE_PATH, TYPE_PATH, "transcripts.txt")

    if not os.path.isfile(META_PATH):
        raise Exception("[error] the metadata file is not found.")

    with open(META_PATH, "r", encoding='utf8') as f:
        for j, line in enumerate(f.readlines(), start=1):
            audio_name = line.split('\t')[0] # ex) 10214_10108_000003
            sub_folder1 = audio_name.split('_')[0] # ex) 10214
            sub_folder2 = audio_name.split('_')[1] # ex) 10108

            audio_path = os.path.join(BASE_PATH, TYPE_PATH, "audio", sub_folder1, sub_folder2, audio_name) + ".flac"
            
            # if the empty file is found, pass through
            if not os.path.isfile(audio_path):
                continue
            
            sentence = line.split('\t')[1]
            sentence = sentence_filter(sentence, mode)
            translated = ipa.convert(sentence)
            
            # if eng_to_ipa couldn't transliterate the word into ipa, sentence_filter returns None
            if '*' in translated:
                continue

            audio_paths.append(audio_path)
            transcripts.append(translated)

    return audio_paths, transcripts
