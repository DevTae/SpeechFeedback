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

import argparse
import torch
import torch.nn as nn
import numpy as np
import torchaudio
import shutil
from torch import Tensor

from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.data.audio.core import load_audio
from kospeech.models import (
    SpeechTransformer,
    Jasper,
    DeepSpeech2,
    ListenAttendSpell,
    Conformer,
)

from ipa_feedback import provide_feedback
import ipa2ko

from fastapi import FastAPI, UploadFile, File
app = FastAPI()

def parse_audio(audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm') -> Tensor:
    signal = load_audio(audio_path, del_silence, extension=audio_extension)
    feature = torchaudio.compliance.kaldi.fbank(
        waveform=Tensor(signal).unsqueeze(0),
        num_mel_bins=80,
        frame_length=20,
        frame_shift=10,
        window_type='hamming'
    ).transpose(0, 1).numpy()

    feature -= feature.mean()
    feature /= np.std(feature)

    return torch.FloatTensor(feature).transpose(0, 1)

# Modified by DevTae@2023
@app.post("/test")
async def ipa_feedback(file: UploadFile = File(...)):
    filename = f"output.wav"

    contents = await file.read()

    with open(filename, "wb") as fp:
        fp.write(contents)

    # 날짜 및 시간 별로 음성 녹음본을 저장할 수 있도록 함. (추후 사용자 별로 통계 자료 및 개인화된 서비스 제공할 수 있도록 함.)
    new_filename, extension = os.path.splitext(filename)
    new_filename = f"{new_filename}_{now.year}_{now.month:02d}_{now.day:02d}_{now.hour:02d}_{now.minute:02d}_{now.second:02d}{extension}"
    shutil.copy(filename, new_filename)

    model_path = "/workspace/kospeech/model.pt" # set here model path you want
    audio_path = filename
    device = "cpu"

    feature = parse_audio(audio_path, del_silence=True)
    input_length = torch.LongTensor([len(feature)])
    vocab = KsponSpeechVocabulary('/workspace/data/aihub_labels.csv')

    model = torch.load(model_path, map_location=lambda storage, loc: storage).to(device)

    if isinstance(model, nn.DataParallel):
        model = model.module
    model.eval()

    if isinstance(model, DeepSpeech2):
        model.device = device
        y_hats = model.recognize(feature.unsqueeze(0), input_length)

    sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())

    # Get the feedback of user_ipa data
    user_ipa = sentence[0]
    standard_ipa = "ɑnnjʌŋɑsɛjo" # default: "안녕하세요"
    feedback = provide_feedback(standard_ipa, user_ipa) # searching the incorrect part in linear method

    # to be implemented to return multiple feedbacks later
    #feedbacks = []

    #if isinstance(feedback, str):
    #    feedbacks.append(feedback)
    #else:
    #    for fb in feedback:
    #        feedbacks.append(fb)

    # Get the string data of user_ipa and standard_ipa in hangul
    #user_ipa_hangul = ipa2ko.ipa_to_hangul(user_ipa, ipa2ko.ipa_dict)
    #standard_ipa_hangul = ipa2ko.ipa_to_hangul(standard_ipa, ipa2ko.ipa_dict)

    # Return all of the data
    return { "answer" : standard_ipa,
               "user" : user_ipa,
               "feedback" : feedback }
