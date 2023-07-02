### SpeechFeedback

- 해당 디렉토리는 **전처리할 때 도움이 되는 파이썬 스크립트 파일들**을 저장해둔 곳입니다.

- `unzip.sh` 파일 의 경우 한국인 음성 데이터셋의 압축 풀기를 쉽게 할 수 있도록 제작해둔 스크립트입니다.

- `preprocess` 관련 파일들은 각 상황에 맞는 전처리 스크립트이며, `kospeech/dataset/kspon/preprocess` 폴더 안의 `preprocess.py` 파일과 비교하여 상황에 맞게 바꾸어 적용하면 됩니다.

- 파일 이름 접두사에 `ipa` 가 붙어 있는 것들은 ipa 문자 관련 작동(ipa 변환값 scraping, converter) 스크립트입니다.

- 파일 이름 접두사에 `audio_data` 가 붙어 있는 것들은 음성 데이터에 대한 확인 작업을 하는 스크립트입니다.

- `wav_timestamp_split.py` 파일의 경우, 간혹 가다가 한 음성 파일 안에 여러 timestamp 에 걸쳐 저장되어 있는 경우가 있는데 그런 상황에 적절하게 사용할 수 있도록 제작해둔 스크립트 파일입니다.