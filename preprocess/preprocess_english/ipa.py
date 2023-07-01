# Copyright (c) 2020, Soohwan Kim. All rights reserved.
# Copyright (c) 2023, DevTae. All rights reserved.
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
import pandas as pd


def load_label(filepath):
    ipa2id = dict()
    id2ipa = dict()

    ipa_labels = pd.read_csv(filepath, encoding="utf-8")

    id_list = ipa_labels["id"]
    ipa_list = ipa_labels["ipa"]
    freq_list = ipa_labels["freq"]

    for (id_, ipa, freq) in zip(id_list, ipa_list, freq_list):
        ipa2id[ipa] = id_
        id2ipa[id_] = ipa
    return ipa2id, id2ipa


def sentence_to_target(sentence, ipa2id):
    target = str()

    for ipa in sentence:
        try:
            target += (str(ipa2id[ipa]) + ' ')
        except KeyError:
            continue

    return target[:-1]


def generate_ipa_labels(transcripts, labels_dest):
    print('create_ipa_labels started..')

    # if you want to merge the ipa characters, set it.
    ipas = list()

    label_list = list()
    label_freq = list()

    for transcript in transcripts:
        idx = 0
        while idx < len(transcript):
            check = False
            ch = transcript[idx]
            if ch != ' ':
                for ipa in ipas:
                    if ipa == transcript[idx:idx+len(ipa)]:
                        check = True
                        ch = ipa
                        idx += len(ipa)
                        break
                if check == False:
                    idx += 1
            else:
                idx += 1

            if ch not in label_list:
                label_list.append(ch)
                label_freq.append(1)
            else:
                label_freq[label_list.index(ch)] += 1

    # sort together Using zip
    label_freq, label_list = zip(*sorted(zip(label_freq, label_list), reverse=True))
    label = {'id': [0, 1, 2], 'ipa': ['<pad>', '<sos>', '<eos>'], 'freq': [0, 0, 0]}

    for idx, (ipa, freq) in enumerate(zip(label_list, label_freq)):
        label['id'].append(idx + 3)
        label['ipa'].append(ipa)
        label['freq'].append(freq)

    label_df = pd.DataFrame(label)
    label_df.to_csv(os.path.join(labels_dest, "aihub_labels.csv"), encoding="utf-8", index=False)


def generate_ipa_script(audio_paths, transcripts, labels_dest):
    print('create_script started..')
    ipa2id, id2ipa = load_label(os.path.join(labels_dest, "aihub_labels.csv"))

    with open(os.path.join("transcripts.txt"), "w") as f:
        for audio_path, transcript in zip(audio_paths, transcripts):
            ipa_id_transcript = sentence_to_target(transcript, ipa2id)
            audio_path = audio_path.replace('txt', 'pcm')
            f.write(f'{audio_path}\t{transcript}\t{ipa_id_transcript}\n')
