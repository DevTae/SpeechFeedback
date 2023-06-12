# SpeechFeedBack

- 현재 디렉토리는 입력된 음성에 대한 피드백을 제공할 수 있는 코드가 있습니다.

- `FastAPI` 를 통하여 `POST 형식`으로 받은 음성에 대한 피드백을 반환하도록 구현하였습니다.

<br/>

- `FastAPI` 설치 메뉴얼
  1. `pip install fastapi`
  2. `pip install uvicorn`

- 필요한 추가 라이브러리 설치 메뉴얼
  1. `pip install panphon`

<br/>

- 모든 설치가 완료되었다면, 해당 디렉토리에서 `bash start.sh` 를 통하여 서버를 실행합니다.
- 그 이후, `ipa_feedback_client.py` 를 통하여 피드백 프로그램을 실행합니다.

