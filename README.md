# SpeechFeedback

End-to-End ASR (Automatic Speech Recognition) Feedback System

**IPA 변환**을 통하여 발음 그대로 인식하도록 하고 그에 대한 **발음 피드백**을 진행할 수 있도록 하는 것이 목표이다.

KoSpeech 툴킷 : [sooftware/kospeech](https://github.com/sooftware/kospeech) 을 활용하여 프로젝트를 진행하였다.

<br/>

### Contents
0. [Environment Setting](#environment-setting)
1. [Docker Image](#docker-image)
2. [How to done Preprocessing (IPA and Character Dictionary)](#how-to-done-preprocessing-ipa-and-character-dictionary)
3. [How to train `Deep Speech 2` model](#how-to-train-deep-speech-2-model)
4. [How to evaluate `Deep Speech 2` model](#how-to-evaluate-deep-speech-2-model)
5. [How to inference the audio file using `Deep Speech 2` model](#how-to-inference-the-audio-file-using-deep-speech-2-model)
6. [Performance After Using IPA](#performance-after-using-ipa)

<br/>

-----

<br/>

### Environment Setting

- 실험 환경
  - Docker Image : [devtae/kospeech](https://hub.docker.com/r/devtae/kospeech)
  - OS : Linux 5.4.0-148-generic x86_64
  - CPU : 12th Gen Intel(R) Core(TM) i9-12900K
  - GPU : (NVIDIA GeForce RTX 4090 24GB) X 2
  - CUDA version : 12.0
  - PyTorch version : 1.9.0+cu111

- 음성 데이터 수집 및 전처리
  - 데이터셋 : [AIHub 한국인 대화음성](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=130)
  - IPA 변환기 : [표준발음 변환기](http://pronunciation.cs.pusan.ac.kr/)
  - IPA 변환기 : [stannam/hangul_to_ipa](https://github.com/stannam/hangul_to_ipa)
    - ipa_converter.py 및 csv 폴더로 변환 완료
  - ipa_converter.py 및 preprocess.py 이용하여 전처리 진행
  - Train : Validation : Test = 270000 : 30000 : 32264

- 하이퍼 파라미터 튜닝
  - num_epochs : 20
  - batch_size : 32
  - optimizer : adam
  - init_lr : 1e-06
  - final_lr : 1e-06
  - peak_lr : 1e-04
  - init_lr_scale : 0.01
  - final_lr_scale : 0.05
    - learning rate 설정의 경우, 데이터와 상황에 따라 다르게 설정될 수 있음.
    - adam optimizer 특성 상, 초반 adaptive learning rate 분산이 매우 커져 local optima 에 도달 가능하므로 초반 lr 비교적 축소시킴.
    - 낮은 batch_size 와 낮은 learning rate 의 조합이 좋음.
  - max_grad_norm : 400
  - warmup_steps : 400
  - weight_decay : 1e-05
  - hidden_dim : 1024
  - dropout : 0.3
  - num_encoder_layers : 3
  - rnn_type : gru
  - max_len : 400
    - 데이터 출력층에 따라 다르게 설정 가능
  - spec_augment : **false**
    - 빠른 러닝을 위하여 비활성화하였음

<br/>

### Docker Image

KoSpeech (Using CUDA 12.0) : https://hub.docker.com/r/devtae/kospeech

1. `sudo docker run -it --gpus all --name devtae -v {하위 디렉토리}/한국인\ 대화\ 음성/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data:/workspace/data devtae/kospeech`
    - 공유 디렉토리 기능을 사용하여, `{하위 디렉토리}/한국인\ 대화\ 음성/Training/data/remote/PROJECT/AI학습데이터/KoreanSpeech/data` 폴더에 있는 파일들이 `/workspace/data` 과 연동된다.

2. `sudo docker attach devtae`

또는 [sooftware/kospeech](https://github.com/sooftware/kospeech) 를 Clone 하여 사용할 것.

<br/>

### How to done Preprocessing (IPA and Character Dictionary)

1. ipa_crawl.py 과 ipa_preprocess.py *(부산대학교 인공지능연구소의 허락을 받아야 실행할 수 있음 (중요))* 를 `/workspace/data` 에 넣는다.

    - 만약 converter_ipa.py 를 사용하고자 한다면, `converter_ipa.py` 파일과 `csv` 폴더를 `/workspace/kospeech/dataset/kspon` 에 옮겨놓고 `preprocess.py` 의 transcripts.append 부분에 applyRulesToHangulTotal 함수가 적용될 수 있도록 주석을 해제하여 수정합니다. 이후 `3 번`으로 넘어가면 됩니다.

2. `python3 ipa_preprocess.py` 를 실행하여 데이터에 대한 IPA 변환을 진행한다.

3. `KoSpeech/dataset/kspon/preprocess.sh` **(해당 repo 에서 복사 및 붙여넣기 진행)** 에서의 `DATASET_PATH` 에 `/workspace/data` 를 입력하고 `VOCAB_DEST` 에는 `/workspace/data/vocab` 를 입력한다.

4. `bash preprocess.sh` 를 통해 전처리를 완료한다.

5. 그 결과, `main.py` 가 있던 디렉토리에 `transcripts.txt` 가 생기고, 단어 사전은 설정된 `VOCAB_DEST` *(/workspace/data/vocab)* 폴더에 저장된다.

- 해당 레포에 있는 코드는 `1.Training` 에 대한 데이터를 모두 전처리하는 것이며, `2.Validation` 데이터를 이용하지 않는다. 따라서 별 다른 수정 없이 사용한다면, `1.Training` 에서 원하는 데이터들을 바탕으로 transcripts 를 형성시키고, 그 중에서도 일부를 떼어내 따로 evaluation 용 `transcripts_test.txt` 파일을 만들어 사용하면 된다.

<br/>

### How to train `Deep Speech 2` model

1. `KoSpeech/configs/audio/fbank.yaml` *(melspectrogram.yaml, mfcc.yaml, spectrogram.yaml)* 에서 음원 확장명(.pcm or .wav)을 수정한다.

2. `KoSpeech/kospeech/data/data_loader.py` 에서 train, validation 데이터 수를 설정한다. (transcripts.txt 파일에서의 데이터 수)
    - 만약 train : validation : test 비율을 설정하고자 할 때는, train+validation 만큼 transcripts.txt 에 있도록 하고, 나머지 test 만큼 transcripts_test.txt 에 있도록 한다.
    - train 과 validation 데이터 개수는 data_loader.py 에서 설정한다.

3. main.py, eval.py, inference.py 에 대하여 단어 사전 경로를 `/workspace/data/vocab/aihub_labels.csv` 로 수정해준다.

4. `KoSpeech/configs/train/ds2_train.yaml` 에서 `transcripts_path: '/workspace/kospeech/dataset/kspon/transcripts.txt'` 로 설정한다.

5. 최종적으로, `python ./bin/main.py model=ds2 train=ds2_train train.dataset_path=/workspace/data` 를 실행한다.

- 다음 파일(supervised_trainer.py)에서 cp949 인코딩 방식 때문에 오류가 발생한다면 utf8 로 바꾸어야 한다.

- 만약, CTC Loss 계산식에서 nan 이 뜨는 것을 방지하고 싶다면 **데이터 보정** 및 **하이퍼 파라미터 수정**을 하거나 `torch.nan_to_num(outputs)` 함수를 이용한다.

<br/>

### How to evaluate `Deep Speech 2` model

- 아래 코드를 바탕으로 평가를 진행한다.

- `python ./bin/eval.py eval.dataset_path=/workspace/data eval.transcripts_path=/workspace/kospeech/dataset/kspon/transcripts_test.txt eval.model_path=/workspace/kospeech/outputs/{date}/{time}/model.pt`

<br/>

### How to inference the audio file using `Deep Speech 2` model

- 아래 코드를 바탕으로 해당 오디오 파일에 대하여 추론을 한다.

- `python3 ./bin/inference.py --model_path /workspace/kospeech/outputs/{date}/{time}/model.pt --audio_path /workspace/data/1.Training/2.원천데이터/1.방송/broadcast_01/001/broadcast_00000001.wav --device "cpu"`

<br/>

### Performance After Using IPA

![image](https://github.com/DevTae/SpeechFeedback/assets/55177359/5fb8dd51-dbc6-44ee-aedd-43be06d51e28)

- 단어사전 경우의 수를 **2000 → 34 개**로 축소할 수 있었다.

