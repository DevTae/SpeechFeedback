# SpeechFeedback

End-to-End ASR (Automatic Speech Recognition) Feedback System

<br/>

### Docker Image

KoSpeech (Using CUDA 12.0) : https://hub.docker.com/r/devtae/kospeech

<br/>

### How to done Preprocessing

1. ipa_crawl.py 과 ipa_preprocess.py *(부산대학교 인공지능연구소의 허락을 받아야 실행할 수 있음)* 를 `한국인\ 대화\ 음성/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data` 에 넣는다.

2. `python3 ipa_preprocess.py` 를 실행하여 데이터에 대한 IPA 변환을 진행한다.

3. IPA 변환이 끝난 후, `KoSpeech/dataset/kspon/preprocess.sh` 에서의 `DATASET_PATH` 에 `..../한국인\ 대화\ 음성/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data` 를 입력하고 `VOCAB_DEST` 에는 본인이 원하는 경로 (ex. `/workspace/data/vocab`) 를 입력한다.

4. `bash preprocess.sh` 를 통해 전처리를 완료한다.
