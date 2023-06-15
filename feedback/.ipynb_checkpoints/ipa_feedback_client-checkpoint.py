import sounddevice as sd
import requests
from scipy.io.wavfile import write

# the duration of the recording in seconds
duration = 3.0

# the sample rate (in samples/sec), change this value if needed
sample_rate = 16000

print("\"안녕하세요\" 라고 3초 내에 말씀해보세요.")
      
# use the sounddevice library to record audio
print("녹음 시작...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()  # wait until the recording is done
print("녹음 완료.")

# use the scipy library to save the numpy array into a .wav file
write("output.pcm", sample_rate, recording)

# 서버에 음성 인식 결과에 대하여 요청하기
url = "http://127.0.0.1:8000/test" # link to fastAPI server (setting on your IP later)
files = {"file": open("output.pcm", "rb")} # read in binary format

# 서버 요청 결과 출력하기
# 정답(ɑnnjʌŋɑsɛjo)과 입력 사이의 피드백
response = requests.post(url, files=files)
print(response.content.decode('utf8'))
