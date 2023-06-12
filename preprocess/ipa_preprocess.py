# Developed by DevTae@2023
# Using the bracket_filter and special_filter function from sooftware/KoSpeech
import os
import re
import ipa_crawl as ipa

# get all folder path of metadatas
# AIHub '한국인 대화음성' 데이터셋
def get_all_path():
    BASE_PATH = os.getcwd()
    META_PATH = "/1.Training/1.라벨링데이터/{THEME_FOLDER}/{THEME_LABEL}_{NUM}/{THEME_LABEL}_{NUM}_metadata.txt"
    THEME_INFO = { "1.방송" : [ "broadcast", 5 ],
                   "2.취미" : [ "hobby", 1 ],
                   "3.일상안부" : [ "dialog", 4 ],
                   "4.생활" : [ "life", 10 ],
                   "5.날씨" : [ "weather", 3 ],
                   "6.경제" : [ "economy", 4 ],
                   "7.놀이" : [ "play", 2],
                   "8.쇼핑" : [ "shopping", 2] }
    
    paths = []
    for key, value in THEME_INFO.items():
        for i in range(1, value[1] + 1, 1):
            metafile = BASE_PATH + META_PATH.replace("{THEME_FOLDER}", key).replace("{THEME_LABEL}", value[0]).replace("{NUM}", "{0:0>2d}".format(i))
            paths.append(metafile)
    return paths

# filter the bracket
# from sooftware/KoSpeech
def bracket_filter(sentence):
    new_sentence = str()
    flag = False

    for ch in sentence:
        if ch == '(' and flag == False:
            flag = True
            continue
        if ch == '(' and flag == True:
            flag = False
            continue
        if ch != ')' and flag == False:
            new_sentence += ch
    return new_sentence

# Edited by DevTae
# filter the special character
# from sooftware/KoSpeech
def special_filter(sentence, mode='phonetic', replace=None):
    new_sentence = str()
    for idx, ch in enumerate(sentence):
        if re.search(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ]", ch) is None:
            if not (ch == '!' or ch == '?' or ch == '.' or ch == ',' or ch == ' '):
                return None
        new_sentence += ch

    pattern = re.compile(r'\s\s+') # 스페이스바 두 번 이상일 때
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence

# main function
def start():
    BASE_PATH = os.getcwd()
    for i, path in enumerate(get_all_path(), start=1):
        f = open(path, "r", encoding="utf8")
        ipa_f = open(path.replace(".txt", "_ipa.txt"), "a", encoding="utf8")

        for j, line in enumerate(f.readlines(), start=1):
            datas = line.split('|')
            # 서울/경기 이외에는 생략 (표준어 위주 학습)
            if not datas[6].strip() != "1":
                continue;

            txt_file_name = datas[0].strip().replace(".wav", ".txt")
            ipa_file_name = txt_file_name.replace(".txt", "_ipa.txt")

            # 이미 불러온 데이터라면 생략
            if os.path.isfile(BASE_PATH + ipa_file_name):
                print("[continue] {} already exists".format(ipa_file_name))
                continue

            # 만약 라벨링 파일이 없다면 생략
            if not os.path.isfile(BASE_PATH + txt_file_name):
                print("[continue] {} is not found".format(txt_file_name))
                continue

            label_f = open(BASE_PATH + txt_file_name, "r", encoding="utf8")

            filtered = special_filter(bracket_filter(label_f.read()))
            if filtered == "" or filtered None: # 변환할 텍스트가 없거나 None 일 때 ipa 변환 취소
                label_f.close()
                continue
            
            converted = ipa.get_ipa_sentence(filtered)
            if converted is None: # 변환된 텍스트가 없을 시 ipa 변환 취소
                label_f.close()
                continue;

            ipa_label_f = open(BASE_PATH + ipa_file_name, "w", encoding="utf8")
            ipa_label_f.write(converted)
            ipa_label_f.close()
            label_f.close()
            ipa_f.write(line)
            print("[done] ({}, {}) {}".format(i, j, ipa_file_name))

        f.close()
        ipa_f.close()

start()

