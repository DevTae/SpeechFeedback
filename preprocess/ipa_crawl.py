# Developed by DevTae@2023
# 표준발음 변환기 사이트를 바탕으로 IPA 발음을 반환하는 코드입니다.
# 스크래핑을 하시려면 부산대학교 정보컴퓨터공학부 인공지능연구실에 직접 허가를 받으신 후 사용해야 합니다.

import requests
import html
import time

# word 에 대한 ipa 를 가져온 뒤 반환해줌. 실패 시, None 반환
def get_ipa_word(word):
    session = requests.session()
    url = "http://pronunciation.cs.pusan.ac.kr/pronunc2.asp?text1="
    url2 = "&submit1=%C8%AE%C0%CE%C7%CF%B1%E2"
    target = word
    target_encoded = target.encode("euc-kr")
    target_url = ""
    
    for byte in target_encoded:
        target_url += '%{0:0>2X}'.format(byte)
   
    while True:
        try:
            response = session.get(url + target_url + url2)
            response.encoding = "euc-kr" # apparent_encoding 사용 가능
            
            if response.status_code == 200:
                try:
                    modified_target = response.text.split("<td class=td2 > ")[1].split("\r\n")[0]
                    ipa_of_target = html.unescape(response.text.split("<td class=td2 >")[3].split("\r\n")[0].split("/")[0])
                except: # 변환 실패한 경우
                    print("[continue] word error. word is {}".format(word))
                    return None
            
                if target == modified_target:
                    #print(modified_target)
                    #print(ipa_of_target)
                    #f = open("broadcast_00000001.txt", 'w', encoding='utf8')
                    #f.write(ipa_of_target)
                    #f.close()
                    return ipa_of_target
                else: # 변환 결과가 다른 경우
                    print("[continue] words are not equal")
                    return None
            elif "An error occurred on the server when processing the URL" in response.text: # 특정 단어 URL에 대한 오류 발생 경우
                print("[continue] url error")
                return None
            else:
                print("[exception] exception in status code")
                print(response.text)
                raise Exception

        except Exception as e: # 그외의 모든 예외에 대하여 sleep 처리
            print("[sleep] exception handling occured! sleep 10 sec")
            print(e)
            time.sleep(10)
            session = requests.session()

# sentence 에 대한 ipa 를 가져온 뒤 반환해줌. 실패 시, None 반환
def get_ipa_sentence(sentence):
    words = sentence.split(" ")
    result = str()

    for word in words:
        ipa_of_word = get_ipa_word(word)
        if ipa_of_word is not None:
            if result != "":
                result += " "
            result += ipa_of_word
        else:
            return None

    return result

#sentence = "안녕하세요 저는 김태현입니다"
#print(get_ipa_sentence(sentence))

#sentence = "예쁜 사과"
#print(get_ipa_sentence(sentence))

#sentence = "맛있는 고구마"
#print(get_ipa_sentence(sentence))

