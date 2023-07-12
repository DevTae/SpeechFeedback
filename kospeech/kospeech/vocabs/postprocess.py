# Developed by DevTae@2023
# 만약, IPA 설정이 바뀐다면 수정할 것.

class PostProcess:
    def __init__(self):
        # 해당 consonants 및 vowels 변수는 언어 변경 및 IPA 테이블 변경 시 동일하게 변경해주어야 합니다.
        self.consonants = [ 'b', 'bʰ', 'b*', 'p', 'pʰ', 'p*', 'm', 'd', 'dʰ', 'd*', 't', 'tʰ', 't*', 's', 's*', 'n', 'ɾ', 'l', 'dʑ', 'dʑʰ', 'dʑ*', 'tɕ', 'tɕʰ', 'tɕ*', 'ɡ', 'ɡʰ', 'ɡ*', 'k', 'kʰ', 'k*', 'ŋ', 'h' ]
        self.consonants = sorted(self.consonants, key=lambda x: len(x), reverse=True)
        self.vowels = [ 'i', 'ɯ', 'u', 'ɛ', 'ʌ', 'o', 'ɑ', 'a', 'ju', 'jʌ', 'jo', 'jɛ', 'ja', 'wi', 'wʌ', 'wɛ', 'wa', 'ɰi' ]
        self.vowels = sorted(self.vowels, key=lambda x: len(x), reverse=True)
        
    def sanitize(self, data: str):
        data = data.replace("<pad>", "")
        data = data.replace("<sos>", "")
        data = data.replace("<eos>", "")
        data = data.replace("<blank>", "")
        data = data.replace("  ", " ")
        
        sentence = str()
        list_of_sentence = list()
        types = str()
        
        idx = 0
        blank = ' '
    
        while idx < len(data):
            if data[idx] == blank:
                sentence += blank
                list_of_sentence.append(blank)
                types += blank
                idx += 1
            else:
                find = False
                
                for consonant in self.consonants:
                    if idx+len(consonant) <= len(data) and data[idx:idx+len(consonant)] == consonant:
                        find = True
                        prev = list_of_sentence[-1] if len(list_of_sentence) > 0 else None
                        now = data[idx:idx+len(consonant)]
                        now_type = 'C' if consonant != 'ŋ' else 'c' # 받침자음일 때, c 로 추가
                        
                        if not self.check_duplicated(prev, types, now, now_type):
                            sentence += now
                            list_of_sentence.append(now)
                            types += now_type

                        idx += len(consonant)
                        break

                for vowel in self.vowels:
                    if idx+len(vowel) <= len(data) and data[idx:idx+len(vowel)] == vowel:
                        find = True
                        prev = list_of_sentence [-1] if len(list_of_sentence) > 0 else None
                        now = data[idx:idx+len(vowel)]
                        now_type = 'V'

                        if not self.check_duplicated(prev, types, now, now_type):
                            sentence += now
                            list_of_sentence.append(now)
                            types += now_type

                        idx += len(vowel)
                        break

                if find == False:
                    raise Exception("Exception occured in kospeech/vocabs/ksponspeech.py:sanitize function! the other labeling data not in aihub_labels.csv was entered")
                                    
        return sentence

    def check_duplicated(self, prev, prev_types, now, now_type):
        if prev != now: # 이전 문자와 다른 경우 False
            return False
        else: # 이전 문자와 같으면서
            if now_type == 'V': # 같은 모음이 두 번 이상 나온 경우
                return True
            elif now_type == 'c': # 받침 자음이 두 번 동일하게 나온 경우
                return True
            elif now_type == 'C':
                if prev_types.endswith("CC"): # 받침자음에 그 다음 자음까지 나온 상황, 즉, 자음이 세 번 이상 나온 경우
                    return True
                elif prev_types.endswith(" C") or len(prev_types) == 1: # 처음부터 자음만 두 개 이상 나온 경우
                    return True
                
        return False

"""
tool = PostProcess()
datas = [ " bʰbʰbʰbʰbʰ",
          "ɑnnjʌŋɑsɛjo",
          "ɑnnjʌŋɑsɛjo ɑnnjʌŋɑsɛjo",
          "ɑndɛʌmɑnsɛjo",
          "hɑnnjʌŋ kɑssɛjo",
          "mjʌŋŋwadʑi  mjʌŋŋɑɑndʑɛo",
          "a",
          "b",
          " ",
          "" ]

for data in datas:
    print(tool.sanitize(data))
"""
