# Developed by DevTae@2023

import os
import numpy as np

path = "/workspace/kospeech/dataset/kspon/transcripts.txt"
length_data = list()

if os.path.isfile(path):
    with open(path, "r", encoding="utf8") as f:
        for line in f.readlines():
            length_data.append(len(line.split('\t')[1]))
        print("max is", max(length_data))
        print("min is", min(length_data))
        print("avg is", sum(length_data)/len(length_data))
        print("np.percentile is")
        print(np.percentile(length_data, q=[0, 25, 50, 75, 100]))
        # max is 1128
        # min is 3
        # avg is 74.08081333333334
        # np.percentile is
        # [ 3. 36. 56. 91. 1128. ]
        # lstm max_len is set to be 100.
else:
    print("could not find the transcripts.txt")
