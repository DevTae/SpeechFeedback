### SpeechFeedback

- `.pcm` 확장명이 아닌 음성 파일로 `Evaluation` 을 진행했을 때 뜨는 `Audio is None` 현상 해결 방법

  - 음성 파일 확장명을 `.pcm` 이 아닌 `.wav` 으로 진행했을 때, Evaluation 과정에서 오류가 생긴다.

  - 그 이유는 `audio_extension` 을 지정해주는 `Training` 과정에 비하여 `Evaluation` 과정에서는 기본값인 `.pcm` 이 들어가기 때문이다.

  - 따라서, `kospeech/data/audio/parse.py` 파일에서 `parse_audio` 함수의 인자 값을 특정 음성 파일 확장명으로 변경하면 된다.
 
  ```python
  # pcm -> wav 로 변경한 예시는 다음과 같음
  def parse_audio(self, audio_path: str, augment_method: int) -> Tensor:
      ...
      signal = load_audio(audio_path, self.del_silence, extension="wav")
      ...
  ```
  
