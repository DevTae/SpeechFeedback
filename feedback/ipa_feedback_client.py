import sounddevice as sd
import requests
from scipy.io.wavfile import write
import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import json
import sys

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
print(response.content.decode('utf8')) # standard_ipa, user_ipa, feedback 출력

feedback_data = response.content.decode('utf8')

# json 내용을 배열에 저장
parsed_data = json.loads(feedback_data)

# 만약 틀린 것이 없으면
if parsed_data["feedback"]["success"] == True:
    print("잘하셨습니다!")
    sys.exit(0) # 프로그램 종료

else:
    # 피드백 결과에 대한 before 문자열을 배열에 저장
    before = parsed_data["feedback"]["before"]
    # 피드백 결과에 대한 after 문자열을 배열에 저장
    after = parsed_data["feedback"]["after"]

    print(before)
    print(after)


# 한국어 ipa에 맞게 매핑하는 파트
csv_file = "../kospeech/bin/csv/ipa2ko.csv"
df = pd.read_csv(csv_file)
#매핑함수정의
def apply_mapping(row):
    # before의 값에 해당하는 Korean값 
    before_value = row["before"]
    before_korean = df.loc[df["IPA"] == before_value, "Korean"].values
    
    # after의 값에 해당하는 Korean값 
    after_value = row["after"]
    after_korean = df.loc[df["IPA"] == after_value, "Korean"].values
    
    if len(before_korean) == 0 or len(after_korean) == 0:
        raise ValueError("한국어 IPA에 매칭되는 결과가 없습니다.")
    
    # 변경된 값 반환
    return before_korean[0], after_korean[0]

#before과 after 배열에 대한 매핑 적용
before_new = []
after_new = []
for i in range(len(before)):
    try:
        before_korean, after_korean = apply_mapping({"before": before[i], "after": after[i]})
        before_new.append(before_korean)
        after_new.append(after_korean)
    except ValueError as e:
        before_new.append("한국어 IPA에 매칭되는 결과가 없습니다.")
        after_new.append("한국어 IPA에 매칭되는 결과가 없습니다.")
#변경 출력
print(before_new)
print(after_new)


#맞는 GUI 출력
class GUIWindow:
    def __init__(self, root, before_new, after_new):
        self.root = root
        self.root.title("발음 교정 피드백")
        self.root.geometry("800x500")
        self.load_images_from_csv('csv/ko2pic.csv')
        self.image_index = 0

        # 이미지 및 설명을 표시할 라벨 생성
        self.title_label = tk.Label(self.root, text="", font=("Arial", 24, "bold"), pady=20)
        self.title_label.pack()

        self.label_frame = tk.Frame(self.root)
        self.label_frame.pack(pady=20)

        self.before_image_label = tk.Label(self.label_frame, padx=20, pady=20)
        self.before_image_label.pack(side='left', padx=10)
        self.arrow_label = tk.Label(self.label_frame, padx=20, pady=20)
        self.arrow_label.pack(side='left', padx=10)
        self.after_image_label = tk.Label(self.label_frame, padx=20, pady=20)
        self.after_image_label.pack(side='left', padx=10)

        # 입력 받는 창과 버튼 생성
        self.before_new = before_new
        self.after_new = after_new
        self.current_index = 0

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.next_button = tk.Button(self.button_frame, text="다음", command=self.show_next_image, state='disabled')
        self.next_button.pack(side='left', padx=10)

        self.close_button = tk.Button(self.button_frame, text="닫기", command=self.root.destroy, state='disabled')
        self.close_button.pack(side='left', padx=10)

        self.arrow_image = Image.open("res/right_arrow.png").resize((50, 50))
        self.arrow_photo = ImageTk.PhotoImage(self.arrow_image)

        self.show_image_and_description()

    def show_image_and_description(self):
        if self.current_index >= len(self.before_new):
            self.before_image_label.configure(text="완벽합니다!")
            self.after_image_label.configure(text="")
            self.arrow_label.configure(image="", text="")
            self.next_button.configure(state='disabled')
            self.close_button.configure(state='normal')
        else:
            before_value = self.before_new[self.current_index]
            after_value = self.after_new[self.current_index]
            if before_value in self.feedback_dict:
                before_image_path = self.feedback_dict[before_value][0]
                before_image = Image.open(before_image_path).resize((300, 300))
                before_photo = ImageTk.PhotoImage(before_image)
                self.before_image_label.configure(image=before_photo, text="")
                self.before_image_label.image = before_photo

                if after_value in self.feedback_dict:
                    after_image_path = self.feedback_dict[after_value][0]
                    after_image = Image.open(after_image_path).resize((300, 300))
                    after_photo = ImageTk.PhotoImage(after_image)
                    self.after_image_label.configure(image=after_photo, text="")
                    self.after_image_label.image = after_photo
                else:
                    self.after_image_label.configure(image="", text="피드백이 존재하지 않습니다.")

                description_text = f"{before_value} 발음을 {after_value}로 발음해보세요!"
                self.title_label.configure(text=description_text)

                if self.current_index < len(self.before_new) - 1:
                    self.arrow_label.configure(image=self.arrow_photo, text="")
                    self.next_button.configure(state='normal')
                    self.close_button.configure(state='disabled')
                else:
                    self.arrow_label.configure(image=self.arrow_photo, text="")
                    self.next_button.configure(state='disabled')
                    self.close_button.configure(state='normal')
            else:
                self.before_image_label.configure(image="", text="피드백이 존재하지 않습니다.")
                self.after_image_label.configure(image="", text="")
                self.arrow_label.configure(image="", text="")
                self.next_button.configure(state='disabled')
                self.close_button.configure(state='normal')

    def show_next_image(self):
        if self.current_index < len(self.before_new) - 1:
            self.current_index += 1
            self.show_image_and_description()

    def load_images_from_csv(self, csv_file):
        df = pd.read_csv(csv_file)
        self.feedback_dict = {}
        for index, row in df.iterrows():
            korean_char = row['korean']
            picture_path_1 = row['picture_path_1']
            picture_paths = [pic for pic in [picture_path_1] if pd.notnull(pic)]
            self.feedback_dict[korean_char] = picture_paths

root = tk.Tk()
gui_window = GUIWindow(root, before_new, after_new)
root.mainloop()
