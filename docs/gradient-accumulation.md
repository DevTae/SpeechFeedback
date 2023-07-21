## Gradient Accumulation 적용 방법
### Developed by DevTae@2023

-----

- 아래 방법으로 GPU 메모리가 부족한 상황 등에서도 높은 batch_size 를 바탕으로 학습할 수 있음.

- `configs/train/ds2_train.yaml` 에서 `batch_size` 수정
  - `batch_size (=real_batch_size) = (desired_batch_size) / (accumulation_step)`
    - = 32 batch_size / 8 steps = 4 batch_size

- `configs/train/ds2_train.yaml` 에서 `warmup_step` 수정 
  - `warmup_step = ((data_count) / (real_batch_size) * (total_epoch) * 0.1) / (accumulation_step)`
    - = (800000 datas / 4 batch_size * 20 epoches * 0.1) / 8 steps = 50000
    - `(data_count) / (real_batch_size)` 는 main.py 으로 train 돌려보았을 때 뜨는 한 에폭 당 스텝 사이즈임.

- `kospeech/trainer/supervised_trainer.py` 에서 `self.optimizer.step` 함수 수정

  - Before
    ```python
    ...
    self.optimizer.step(model)
    ...
    ```

  - After
    ```python
    ...
    # (real_batch_size=4) * (accumulation_step=8) = (batch_size=32) 의 효과
    if (timestep+1) % 8 == 0:
        self.optimizer.step(model)
    ...
    ```
