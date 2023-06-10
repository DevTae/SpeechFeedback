### How to Change the architecture of CNN into the 3-Layer CNN

<br/>

- 현재 KoSpeech 의 Deep Speech 2 에서 지원하는 CNN 은 2-Layer CNN 에 불과하다.
- 따라서, 3-Layer CNN 을 사용하고 싶은 사람들을 위하여 다음 글을 작성하게 되었다.

<br/>

- 일단, 현재 2-Layer CNN 으로 구성되어 있는 코드는 `kospeech/kospeech/models/convolution.py` 에서 확인할 수 있다.

*(in DeepSpeech2Extractor Class ..)*
```python
...
self.conv = MaskCNN(
    nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size=(41, 11), stride=(2, 2), padding=(20, 5), bias=False),
        nn.BatchNorm2d(out_channels),
        self.activation,
        nn.Conv2d(out_channels, out_channels, kernel_size=(21, 11), stride=(2, 1), padding=(10, 5), bias=False),
        nn.BatchNorm2d(out_channels),
        self.activation,
    )
)
...
```

- 코드를 확인해보면, `in_channels → out_channels → out_channels` 으로 `1 → 32 → 32` 방식이 적용된다는 것을 볼 수 있다.
- 필자의 경우에는 IPA 인식을 하기 위하여 세밀한 인식이 필요하므로 3-Layer CNN 방식인 `1 → 32 → 32 → 96` 을 원했다.
  - 해당 방식은 `Mozilla` 의 `Deep Speech 2` 논문을 바탕으로 최고 성능이 나오게 된 구조임.
- 따라서, 다음 코드와 같이 변경해주면 된다.

```python
...
self.conv = MaskCNN(
    nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size=(41, 11), stride=(2, 2), padding=(20, 5), bias=False),
        nn.BatchNorm2d(out_channels),
        self.activation,
        nn.Conv2d(out_channels, out_channels, kernel_size=(21, 11), stride=(2, 1), padding=(10, 5), bias=False),
        nn.BatchNorm2d(out_channels),
        self.activation,
        nn.Conv2d(out_channels, 96, kernel_size=(21, 11), stride=(2, 1), padding=(10, 5), bias=False),
        nn.BatchNorm2d(96),
        self.activation,
    )
)
...
```

- 또한, 이것만 바꾸면 이후 RNN Layer 에서 dimension 계산 차질이 생기기 때문에 `Conv2dExtractor` Class 에서의 `get_output_lengths` 함수를 수정해주어야 한다.
- 코드는 다음과 같다.

#### Before
```python
...
elif isinstance(self, DeepSpeech2Extractor):
    output_dim = int(math.floor(self.input_dim + 2 * 20 - 41) / 2 + 1)
    output_dim = int(math.floor(output_dim + 2 * 10 - 21) / 2 + 1)
    output_dim <<= 5 # depth
...
```

#### After
```python
...
elif isinstance(self, DeepSpeech2Extractor):
    output_dim = int(math.floor(self.input_dim + 2 * 20 - 41) / 2 + 1)
    output_dim = int(math.floor(output_dim + 2 * 10 - 21) / 2 + 1)
    output_dim = int(math.floor(output_dim + 2 * 10 - 21) / 2 + 1)
    output_dim *= 96 # depth
...
```

- 이후 수정이 완료되면 다시 학습을 시도해본 결과, 모델의 구조가 2-Layer CNN 에서 3-Layer CNN 으로 변경된 것을 볼 수 있다.
