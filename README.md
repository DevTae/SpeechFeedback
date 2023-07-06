# SpeechFeedback

End-to-End ASR (Automatic Speech Recognition) Feedback System

**IPA 변환**을 통하여 발음 그대로 인식하도록 하고 그에 대한 **발음 피드백**을 진행할 수 있도록 하는 것이 목표이다.

KoSpeech 툴킷 : [sooftware/kospeech](https://github.com/sooftware/kospeech) 을 활용하여 프로젝트를 진행하였다.

Baidu Research – Silicon Valley AI Lab, [*Deep Speech 2: End-to-End Speech Recognition in English and Mandarin*](https://arxiv.org/pdf/1512.02595v1.pdf), Computation and Language, Dec 2015
  - 다음 논문에서의 모델 구조를 참고하였습니다.

장민정, 정선진, 노준용, [*한국어 동시조음 모델에 기반한 스피치 애니메이션 생성*](http://journal.cg-korea.org/archive/view_article?pid=jkcgs-26-3-49), 컴퓨터그래픽스학회, Jun 2020
  - 다음 논문에서의 혀 모델 시각 자료를 활용하였습니다.

<br/>

### Contents
0. [Folder Structure](#folder-structure)
1. [Environment Setting](#environment-setting)
2. [Docker Image](#docker-image)
3. [How to done Preprocessing (IPA and Character Dictionary)](#how-to-done-preprocessing-ipa-and-character-dictionary)
4. [Model Architecture](#model-architecture)
5. [How to train Deep Speech 2 model](#how-to-train-deep-speech-2-model)
6. [How to evaluate Deep Speech 2 model](#how-to-evaluate-deep-speech-2-model)
7. [How to inference the audio file using Deep Speech 2 model](#how-to-inference-the-audio-file-using-deep-speech-2-model)
8. [Performance After Using IPA](#performance-after-using-ipa)
9. [ETC](#etc)

<br/>

-----

### Folder Structure

```
📦SpeechFeedback
 ┣ 📂docs
 ┣ 📂feedback       // 음성 피드백 기능 시연을 위한 클라이언트 코드
 ┣ 📂kospeech
 ┃ ┣ 📂bin          // 모델 학습, 평가, 추론 함수가 있음. FastAPI 서버로 음성 피드백 정보 제공.
 ┃ ┣ 📂configs      // 모델 하이퍼파라미터 설정
 ┃ ┣ 📂dataset
 ┃ ┃ ┗ 📂kspon      // 데이터셋에 대한 전처리 작업공간
 ┃ ┣ 📂docs
 ┃ ┣ 📂kospeech
 ┃ ┗ 📂test
 ┣ 📂preprocess     // 데이터 전처리를 위한 코드 꾸러미 (kospeech 폴더에는 이미 반영됨)
 ┗ 📂data           // 해당 디렉토리에 KsponSpeech 데이터셋 다운
```

<br/>

### Environment Setting

- 실험 환경
  - Docker Image : [devtae/kospeech](https://hub.docker.com/r/devtae/kospeech)
  - OS : Linux 5.4.0-148-generic x86_64
  - CPU : 12th Gen Intel(R) Core(TM) i9-12900K
  - GPU : (NVIDIA GeForce RTX 4090 24GB) X 2
  - CUDA version : 12.0
  - PyTorch version : 1.9.0+cu111

<br/>

### Docker Image

KoSpeech (Using CUDA 12.0) : https://hub.docker.com/r/devtae/kospeech

1. `sudo docker run -it --gpus all --name devtae -v {하위 디렉토리}/한국어\ 음성:/workspace/data devtae/kospeech`
    - 공유 디렉토리 기능을 사용하여, `{하위 디렉토리}/한국어\ 음성` 폴더에 있는 파일들이 `/workspace/data` 과 연동된다.
    - 원활한 공유 디렉토리 설정을 위하여 데이터셋 다운로드 후에 수행하는 것을 추천한다.

2. `sudo docker attach devtae` 를 실행한 뒤, Docker 이미지 내에서 작업한다.

3. 현재 레포를 `clone` 하여 kospeech 폴더를 workspace 폴더 안에 넣고 작업을 진행한다.

<br/>

### How to done Preprocessing (IPA and Character Dictionary)

- 음성 데이터 수집 및 전처리
  - 데이터셋 : [AIHub 한국어 음성](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123)
  - IPA 변환기 : [표준발음 변환기](http://pronunciation.cs.pusan.ac.kr/)
  - IPA 변환기 : [stannam/hangul_to_ipa](https://github.com/stannam/hangul_to_ipa)
  - 전체 데이터에 대하여 다음과 같이 학습을 진행하였음
    - `Training : Validation : Test = 600000 : 10000 : 10000`

1. `cd SpeechFeedback/kospeech/dataset/kspon` 후에 `bash preprocess.sh` 를 실행하여 전처리를 진행한다.

2. 그 결과, `SpeechFeedback/kospeech/dataset/kspon` 디렉토리에 `transcripts.txt` 와 단어 사전인 `aihub_labels.csv` 가 저장된다.

- 해당 레포에 있는 코드는 Training 데이터에 대해서만 전처리하는 것이며, Evaluation 데이터를 이용하지 않는다. 따라서 별 다른 수정 없이 사용한다면, Training 에서 원하는 데이터들을 바탕으로 transcripts 를 형성시키고, 그 중에서도 일부를 떼어내 따로 evaluation 용 `transcripts_test.txt` 파일을 만들어 사용하면 된다.

<br/>

### Model Architecture

- `Deep Speech 2` 모델 구조
  - **3-Layer CNN**
    - [다음 링크](https://github.com/DevTae/SpeechFeedback/blob/main/docs/how-to-change-into-3-layer-cnn.md)의 메뉴얼을 바탕으로 2-Layer CNN 에서 3-Layer CNN 으로 수정할 수 있음
  - Bi-directional GRU Layer x 7
    - RNN 레이어 수는 하이퍼 파라미터 튜닝에서 설정 가능
  - Fully Connected Layer x 1
  - Batch Normalization
    - 모든 레이어에 momentum=0.99 으로 설정
  - CTC Loss
  - **현재 저장소에는 2-Layer CNN + Bi-directional GRU Layer x 3 으로 구성되어 있음**

- [하이퍼 파라미터 튜닝](https://github.com/DevTae/SpeechFeedback/blob/main/docs/hyper-parameter-tuning.md)
  - Baidu Deep Speech 2 Paper 를 바탕으로 하이퍼 파라미터 튜닝을 진행함.

<br/>

### How to train `Deep Speech 2` model

1. `KoSpeech/kospeech/data/data_loader.py` 에서 train, validation 데이터 수를 설정한다. (transcripts.txt 파일에서의 데이터 수)
    - 만약 train : validation : test 비율을 설정하고자 할 때는, train+validation 만큼 transcripts.txt 에 있도록 하고, 나머지 test 만큼 transcripts_test.txt 에 있도록 한다.
    - train 과 validation 데이터 개수는 data_loader.py 에서 설정한다.

2. `python ./bin/main.py model=ds2 train=ds2_train train.dataset_path=/workspace/data` 를 실행한다.

- (optional) CTC Loss 계산식에서 nan 이 뜨는 것을 방지하고 싶다면 **데이터 보정** 및 **하이퍼 파라미터 수정**을 하거나 `torch.nan_to_num(outputs)` 함수를 이용한다.
  - `torch.nan_to_num(outputs)` 의 경우, 다음 코드와 같이 바꾸면 된다.
  ```Python
  # in kospeech/kospeech/trainer/supervised_learning.py:454L
  ...
  elif architecture in ('deepspeech2', 'jasper'):
      outputs, output_lengths = model(inputs, input_lengths)
      outputs = torch.nan_to_num(outputs)
      loss = self.criterion(
          outputs, targets[:, 1:], contiguous().int(), input_lengths.int(), target_lengths.int()
      )
  ...
  ```

<br/>

### How to evaluate `Deep Speech 2` model

- 아래 코드를 바탕으로 평가를 진행한다.

- `python ./bin/eval.py eval.dataset_path=/workspace/data eval.transcripts_path=/workspace/kospeech/dataset/kspon/transcripts_test.txt eval.model_path=/workspace/kospeech/outputs/{date}/{time}/model.pt`
  - `Beam Search` 진행
  - [parlance/ctcdecode](https://github.com/parlance/ctcdecode)

<br/>

### How to inference the audio file using `Deep Speech 2` model

- 아래 코드를 바탕으로 해당 오디오 파일에 대하여 추론을 한다.

- `python3 ./bin/inference.py --model_path /workspace/kospeech/outputs/{date}/{time}/model.pt --audio_path /workspace/data/{sub_path}/{audio_file}.wav --device "cpu"`

<br/>

### Performance After Using IPA

![23 6 25 aihub_labels csv](https://github.com/DevTae/SpeechFeedback/assets/55177359/b93e5eaa-7af4-44b2-a7df-50eef182b9ab)

- 단어사전 경우의 수(출력층)를 **2000 → 41 개**로 축소할 수 있었다.
- IPA 문자 형태에 맞게 최소 단위로 나뉠 수 있도록 전처리 진행하였다.

![image](https://github.com/DevTae/SpeechFeedback/assets/55177359/01b6e492-6ed4-41a4-adce-0948069db9de)

![23 6 20 Feedback GUI System](https://github.com/DevTae/SpeechFeedback/assets/55177359/70ec3eba-7337-4143-9a94-0700fc92fd61)

- **피드백 알고리즘**을 적용하여 [발음에 대한 피드백](https://github.com/DevTae/SpeechFeedback/tree/main/feedback)을 제공할 수 있게 되었다.

<br/>

### ETC

#### 데이터 종류에 따른 성능 개선
  - 원본 데이터를 직접 들어본 결과, 강의의 오디오를 바탕으로 만든 데이터셋으로 잡음 및 오디오의 전체적인 톤이 높았다.
  - 따라서, [한국인 대화음성](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=130)에서 [한국어 음성](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=123)으로 바꾼 결과, 오디오가 일반인 대화에 적용하기에 더욱 적합함을 확인할 수 있었다.

#### 데이터 라벨링 개수 추가 확보에 따른 성능 개선
  - 이전에는 표준발음 변환기 사이트에서 데이터 수집을 진행하였는데, 사이트 트래픽 문제로 약 1 만 개의 데이터 밖에 훈련에 적용할 수 없는 상태였다.
  - 따라서, 1 epoch 에 대하여 학습되는 양(batch_size=32 기준으로 step size 가 `625 개`)이 적었다.
  - GitHub 에 publish 된 R 코드([stannam/hangul_to_ipa](https://github.com/stannam/hangul_to_ipa))를 바탕으로 IPA 변환해주는 파이썬 스크립트로 변환하였고 데이터 수를 `1 만 개`에서 `60 만 개`까지 늘릴 수 있었다.
  - 그 결과 1 epoch 에 대한 step size 가 `37500 개`로 약 60배 커졌고 동일 epoch 에 대하여 CER 이 향상될 수 있었다.

#### CNN 및 RNN 레이어 수 상승을 통한 성능 개선
  - Deep Speech 2 논문에 있는 내용을 바탕으로 모델 구조를 적용하고자 하였는데, KoSpeech 의 기본 구조는 `CNN * 2, RNN * 3` 으로 구성되어 있었다.
  - Baidu 의 Deep Speech 2 논문에 따르면 `CNN * 3, RNN * 7` 가 성능이 좋다는 것을 찾을 수 있었다.
  - 발음 피드백 시스템 적용을 위하여 심층적인 모델이 필요하다고 판단하였고, 이를 적용하기 위해 [코드를 수정](https://github.com/DevTae/SpeechFeedback/blob/main/docs/3-Layer-CNN.md)할 수 있었다.
  - 그 대신, 레이어가 겹쳐질수록 모델의 복잡성이 올라가 학습 속도가 현저히 느려지므로 해당 trade-off 관계에서 적당한 설정으로 접근하고자 하였다.

#### momentum 계수 수정을 통한 학습 성능 개선
  - Deep Speech 2 논문 내용을 바탕으로 모든 BatchNorm 에 대하여 momentum 계수를 0.99 으로 적용하는 것을 알 수 있었다.
  - 하지만, KoSpeech 의 momentum 계수 기본 설정은 0.1 이었고, 이에 따라, 모든 BatchNorm 에 대하여 momentum 계수에 0.99 를 적용할 수 있었다.
  - 이러한 결과로 기울기에 이전 관성이 적용되어 `local minima 현상을 억제`할 수 있었으며 `CER 감소 추세가 보다 linear 하게` 바뀐 것을 확인할 수 있었다.

#### warmup step 설정을 통한 local minima 현상 개선

![image](https://github.com/DevTae/SpeechFeedback/assets/55177359/7da12595-4393-495b-8c3e-e8d1487f9f63)

(사진 출처 : [sooftware/pytorch-lr-scheduler](https://github.com/sooftware/pytorch-lr-scheduler))

  - adam optimizer 를 바탕으로 한 학습 초반에는 local minima 가 발생할 확률이 높다.
  - 이러한 이유로 KoSpeech 에서는 학습 초반의 learning rate 를 조절하는 warmup step 방식인 TriStageLRSchedule 를 적용하였다.
  - TriStageLRSchedule 스케줄러 알고리즘의 코드를 바탕으로 전체 학습에 대하여 `처음부터 정해진 단계만큼 warmup` 을 하고 `절반까지 최댓값을 유지`했다가 `이후부터는 learning rate 가 감소`하는 방식임을 알 수 있었다.
  - 해당 스케줄러의 warmup 설정 관점을 보아하니 적어도 전체 step size 의 `10%`(=75000)만큼은 warmup step 으로 설정해야겠음을 느꼈고 이를 적용해보았다.
  - 그 결과, 이전(=400)에 대비하여 학습 초반부터 높은 loss와 CER 값에 수렴하는 local minima 를 개선할 수 있었다.

#### 학습 중 무한 로딩(in threading queue)이 걸리는 현상 해결
  - 대용량 데이터를 바탕으로 학습 중 `kospeech/kospeech/trainer/supervised_trainer.py` 의 `queue.get()` 에서 무한 로딩이 걸리게 된다.
  - 이런 경우에 대하여 데드락이 주요한 원인이라고 판단 중이다. 그 이유는 해당 epoch 내에 학습할 데이터 수는 남아있지만, queue 에 대한 get 함수에서 무한대기를 하기 때문이다.
  - 따라서, 해당 문제를 해결하기 위해 queue 에 대하여 동기적으로 접근 후 기다리는 `get` 함수가 아닌 queue 의 원소가 없으면 바로 exception raise 하는 `get_nowait()` 함수를 사용하는 방식으로 해결하였다.
  - 이에 대한 자세한 해결 방법은 해당 [링크](https://github.com/DevTae/SpeechFeedback/blob/main/docs/how-to-solve-the-infinity-loading.md)에서 확인할 수 있다.
