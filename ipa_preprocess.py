# Developed by DevTae@2023
# Using the bracket_filter and special_filter function from sooftware/KoSpeech
# 진행상황 이어가는 기능은 현재 구현하지 않았습니다.
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

# filter the special character
# from sooftware/KoSpeech
def special_filter(sentence):
    SENTENCE_MARK = ['?', '!']
    NOISE = ['o', 'n', 'u', 'b', 'l']
    EXCEPT = ['/', '+', '*', '-', '@', '$', '^', '&', '[', ']', '=', ':', ';', '.', ',']
    EXCEPT += SENTENCE_MARK

    new_sentence = str()
    for idx, ch in enumerate(sentence):
        if ch not in SENTENCE_MARK:
            # o/, n/ 등 처리
            if idx + 1 < len(sentence) and ch in NOISE and sentence[idx+1] == '/':
                continue

        if ch == '#':
            new_sentence += '샾'

        elif ch not in EXCEPT:
            new_sentence += ch

    pattern = re.compile(r'\s\s+')
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence

# main function
def start():
    BASE_PATH = os.getcwd()
    for i, path in enumerate(get_all_path(), start=1):
        f = open(path, "r", encoding="utf8")
        new_f = open(path.replace(".txt", "_ipa.txt"), "w", encoding="utf8")

        for j, line in enumerate(f.readlines(), start=1):
            datas = line.split('|')
            # 서울/경기 이외에는 생략 (표준어 위주 학습)
            if not datas[6].strip() != "1":
                continue;
            txt_file_name = datas[0].strip().replace(".wav", ".txt")
            label_f = open(BASE_PATH + txt_file_name, "r", encoding="utf8")
            ipa_label_f = open(BASE_PATH + txt_file_name.replace(".txt", "_ipa.txt"), "w", encoding="utf8")

            filtered = bracket_filter(special_filter(label_f.read()))
            if filtered == "": # 변환할 텍스트가 없을 시 ipa 변환 취소
                continue

            converted = ipa.get_ipa_sentence(filtered)
            if converted is None:
                label_f.close()
                ipa_label_f.close()
                os.remove(ipa_label_f.name) # 작성된 것이 없을 때는 ipa 파일 삭제 진행
                continue;

            ipa_label_f.write(converted)
            label_f.close()
            ipa_label_f.close()
            new_f.write(line)
            print("[done] ({}, {}) {}".format(i, j, txt_file_name.strip().replace(".txt", "_ipa.txt")))

        f.close()
        new_f.close()

start()
