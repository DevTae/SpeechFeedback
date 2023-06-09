## 개발하고자 하는 모델 종류

#### by DevTae

<br/>

 - 발음에 대한 피드백
   - IPA 와 IPA 사이의 유사도 검사
   - IPA Distance API 활용
   - Deep Speech 2 를 통한 화자의 음성 데이터를 IPA 로 변환한 후, 정답 IPA 와 비교한다.
   - 어떤 부분에서 문제가 있었는지를 파악한 후, 곧바로 발음에 대하여 시각적 피드백을 제공한다. (구강 근육을 근간으로 하여)

<br/>

 - Prosody 에 대한 피드백
   - 언어 화용적 능력에 대한 피드백을 위하여 말빠르기(리듬 및 음장), 높낮이(성조)에 대한 분석을 진행함
   
   - 말빠르기의 경우 ① 단어와 단어 사이, ② IPA 문자와 IPA 문자 사이의 길이를 통해 분류를 진행
   - 말빠르기의 경우 대표적으로 다음과 같은 종류가 있다.
     - 길게
     - 중간
     - 짧게
   
   - 높낮이에 대해서는 단어에 대한 음 높낮이를 파악하여 분류를 진행한다.
   - 높낮이의 경우 대표적으로 다음과 같은 종류가 있다.
     - 유지
     - 상승
     - 상승 후 하락
     - 하락
     - 하락 후 상승
   
   - 위와 같은 종류로 음성 데이터셋을 클러스터링 알고리즘을 바탕으로 분류한 뒤에, 다시금 학습 데이터로 활용하고자 한다.
   - 검증은 실루엣(Silhouette Value)과 Elbow Method, Gap Statistic 를 바탕으로 진행할 것이다.
