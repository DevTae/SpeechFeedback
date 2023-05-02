# Developed by DevTae@2023
# 표준발음 변환기 사이트를 바탕으로 IPA 발음을 반환하는 코드입니다.
# 스크래핑을 하시려면 부산대학교 정보컴퓨터공학부 인공지능연구실에 직접 허가를 받으신 후 사용해야 합니다.

import requests
import html

url = "http://pronunciation.cs.pusan.ac.kr/pronunc2.asp?text1="
url2 = "&submit1=%C8%AE%C0%CE%C7%CF%B1%E2"
target = "있어" # 단어 단위로 입력될 예정
target_encoded = target.encode("euc-kr")
target_url = ""

for byte in target_encoded:
    target_url += '%{0:0>2X}'.format(byte)

response = requests.get(url + target_url + url2)
response.encoding = "euc-kr" # apparent_encoding 사용 가능

if response.status_code == 200:
    #print(response.text)
    modified_target = response.text.split("<td class=td2 > ")[1].split("\r\n")[0]
    ipa_of_target = html.unescape(response.text.split("<td class=td2 >")[3].split("\r\n")[0].split("/")[0])

    if target == modified_target:
        print(modified_target)
        print(ipa_of_target)
        f = open("broadcast_00000001.txt", 'w', encoding='utf8')
        f.write(ipa_of_target)
        f.close()
