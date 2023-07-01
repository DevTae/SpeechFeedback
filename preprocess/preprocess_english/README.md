### SpeechFeedback

- mls_english 데이터셋에 대한 전처리 진행을 위한 파이썬 스크립트 파일입니다.

- 데이터셋의 경우, `mls_download.sh` 를 통해 다운로드를 진행한다. 그리고, `tar_gz_part.sh` 를 통해 압축 해제를 진행한다.

- `kospeech/dataset/kspon/preprocess` 폴더 안에 `ipa.py` 파일과 `preprocess.py` 파일을 넣고, 전처리를 진행한다.

- 현재 영어의 경우, 피드백 기능을 따로 진행하고 있지 않으니 `inference_fastapi.py` 가 아닌 `inference.py` 를 사용하면 된다.