# SpeechFeedback

End-to-End ASR (Automatic Speech Recognition) Feedback System

IPA 변환을 통하여 발음 그대로 인식하도록 하고 그에 대한 발음 피드백을 진행할 수 있도록 하는 것이 목표이다.

데이터셋 : [AIHub 한국인 대화음성](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=130)

<br/>

### Docker Image

KoSpeech (Using CUDA 12.0) : https://hub.docker.com/r/devtae/kospeech

1. `sudo docker run -it --gpus all --name devtae -v {하위 디렉토리}/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data:/workspace/data devtae/kospeech`

2. `sudo docker attach devtae`

<br/>

### How to done Preprocessing

1. ipa_crawl.py 과 ipa_preprocess.py *(부산대학교 인공지능연구소의 허락을 받아야 실행할 수 있음)* 를 `한국인\ 대화\ 음성/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data` 에 넣는다.

2. `python3 ipa_preprocess.py` 를 실행하여 데이터에 대한 IPA 변환을 진행한다.

3. IPA 변환이 끝난 후, `KoSpeech/dataset/kspon/preprocess.sh` (해당 repo 에서 복사 및 붙여넣기 진행) 에서의 `DATASET_PATH` 에 `..../한국인\ 대화\ 음성/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data` 를 입력하고 `VOCAB_DEST` 에는 본인이 원하는 경로 (ex. `/workspace/data/vocab`) 를 입력한다.

4. `bash preprocess.sh` 를 통해 전처리를 완료한다.

5. 그 결과, `main.py` 가 있던 디렉토리에 `transcripts.txt` 가 생기고, 단어 사전은 설정된 `VOCAB_DEST` (ex. /workspace/data/vocab) 폴더에 저장된다.

6. `KoSpeech/configs/audio/fbank.yaml` *(melspectrogram.yaml, mfcc.yaml, spectrogram.yaml)* 에서 음원 확장명(.pcm or .wav)을 수정한다.

7. `KoSpeech/kospeech/data/data_loader.py` 에서 train, validation 데이터 수를 설정한다.

8. main.py, eval.py, inference.py 에 대하여 `단어 사전 경로` *(.vocab)* 를 수정해준다.

9. `KoSpeech/configs/train/ds2_train.yaml` 에서 `transcripts_path: '/workspace/kospeech/dataset/kspon/transcripts.txt'` 로 설정한다.

10. 최종적으로, `python ./bin/main.py model=ds2 train=ds2_train train.dataset_path=/workspace/data` 를 실행한다.

