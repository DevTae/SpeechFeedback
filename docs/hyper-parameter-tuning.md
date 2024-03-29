## 하이퍼 파라미터 튜닝
  - num_epochs : 20
  - batch_size : **128**
  - optimizer : '**adamp**'
    - [clovaai/AdamP](https://github.com/clovaai/AdamP)
  - init_lr : **1e-05**
  - final_lr : **1e-05**
  - peak_lr : **1e-03**
    - learning rate 설정의 경우, 데이터와 상황에 따라 다르게 설정될 수 있음
  - init_lr_scale : 0.01
  - final_lr_scale : 0.05
  - max_grad_norm : **4**
  - warmup_steps : **75000**
    - adam optimizer 특성 상, 초반 adaptive learning rate 분산이 매우 커져 local optima 에 도달 가능하므로 초반 lr 비교적 축소시킴
    - 너무 빠르게 warming-up (Tri-Stage Learning Rate Scheduler 사용) 하게 된다면 local optima 에 갇힐 수 있음
    - `(적정값) = (total_step) * (total_epoch) * 0.05 = ((train 데이터 수) / (batch_size) * (spec_augment ? 5 : 4)) * (total_epoch) * 0.05`
      - ex) `(600000 datas / 32 * 4) * 20 epoches * 0.05 = 75000`
      - 현재, 기본적으로 적용되는 Augmentation 전략이 총 3 가지가 있기 때문에 기본값은 4 로 적용됨
  - weight_decay : **1e-04**
  - reduction : **mean**
  - bidirectional : True
  - use_bidirectional : True
  - hidden_dim : **512** (when using RNN x 3 and you want speedy) 또는 **1880** (when using RNN x 3) 또는 **1280** (when using RNN x 7)
  - dropout : **0.3**
  - num_encoder_layers : **3** 또는 **7**
    - RNN 레이어 개수에 따라 학습 성능 차이가 많이 나는 것을 확인
    - hidden_dim 이 높은 것보다는 num_encoder_layers 가 높은 것이 성능에 더 좋은 영향을 끼침
    - 빠른 학습 속도를 원한다면 hidden_dim 과 num_encoder_layers 둘다 낮은 수치로 사용할 수도 있음
  - rnn_type : **gru**
    - Baidu 의 Deep Speech 2 Paper 에서 제안한 RNN Layer Type 임
  - max_len : **400**
    - 데이터셋에 따라 달라지긴 하지만 해당 수치로 사용하는 것을 추천
  - activation : **clipped_relu**
    - Deep Speech 2 논문 내용에 따라 최솟값이 `0` 이고, 최댓값이 `20` 이 되는 `Clipped ReLU` 를 적용하였음
  - spec_augment : False
