# SpeechFeedback

by DevTae

- 현재 해당 디렉토리에서 `ipa_feedback_client.py` 파일을 통해 서버에 요청하고 그에 대한 피드백을 받을 수 있습니다.

- `ipa_feedback_client.py` 파일을 실행하기 전에 [`SpeechFeedback/kospeech/bin`](https://github.com/DevTae/SpeechFeedback/tree/main/kospeech/bin) 폴더에 진입하여 FastAPI 서버를 실행해주세요.

- 이후 FastAPI 서버가 실행되는 것을 확인한 뒤에, `python ipa_feedback_client.py` 를 실행합니다.

- 프로그램에서 안내하는 내용대로 마이크에 `안녕하세요` 라고 말한 뒤에 그에 대한 피드백을 확인할 수 있습니다.

- 서버에서 반환하는 json 타입 포맷은 다음과 같습니다.

``` python
parsed_data =
 { "answer" : "정답 IPA",
   "user" : "유저 IPA",
   "feedback" : { "success" : "성공 여부", "before" : "교정 전", "after" : "교정 후" } }
```
