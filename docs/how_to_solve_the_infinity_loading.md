### 딥러닝 학습 중 무한 대기 현상을 해결하는 방식

- 대용량 데이터를 바탕으로 학습하던 도중 공유 자원 `queue` 에 대한 `get` 을 진행하지 못하여 Ctrl + C 를 통하여 강제 종료하는 상황이 종종 생기곤 한다.

- 이런 경우에 대하여 데드락이 주요한 원인이라고 판단 중이다. 그 이유는 해당 epoch 내에 학습할 데이터 수는 남아있지만, queue 에 대한 get 함수에서 무한대기를 하기 때문이다.

- 따라서, 해당 문제를 해결하기 위해 queue 에 대하여 동기적으로 접근 후 기다리는 `queue.get()` 함수가 아닌 queue 의 원소가 없으면 바로 exception raise 하는 `queue.get_nowait()` 함수를 사용하는 방식으로 해결하였다.


- 다음 코드 `kospeech/kospeech/trainer/supervised_trainer.py` 에서 다음과 같이 수정하고 학습을 진행하면 동일한 문제 발생 시 해당 epoch 에 남은 데이터를 생략하고 다음 epoch 으로 넘어갈 수 있다.

#### Before

```python
inputs, targets, input_lengths, target_lengths = queue.get()

if inputs.shape[0] == 0:
```

#### After
```python
infinity_loading = False
trial  = 10

# try 10 times when infinity loading occured
for i in range(1, trial+1):
    try:
        inputs, targets, input_lengths, target_lengths = queue.get_nowait()
        break # if queue.get_nowait returned successfully, escape from here
    except:
        # after the 10 trial are done, escape from here if infinity loading is remaining
        if i == trial:
            infinity_loading = True
            print([Skip] Even though trying 10 times, it was unsuccessful to load datas. Skip it..")
        else:
            time.sleep(1)

if infinity_loading or inputs.shape[0] == 0:
```
