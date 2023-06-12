#pip install panphon

from panphon.featuretable import FeatureTable

def provide_feedback(standard_ipa, user_ipa):
    ft = FeatureTable()
    features = ['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    
    standard_ipa_list = list(standard_ipa)
    user_ipa_list = list(user_ipa)
    
    #if len(standard_ipa_list) != len(user_ipa_list):
    #    return "다시 시도하세요."
    
    standard_array = ft.word_array(features, standard_ipa)
    user_array = ft.word_array(features, user_ipa)
    
    feedback = []
    
    # Developed by DevTae@2023
    # 정답 labeling index 를 기준으로 삼고 한 개씩 오른쪽으로 포인터를 옮기면서 조건을 확인합니다.
    # 입력 labeling index 에서 같은 문자가 나오지 않으면 바로 피드백합니다.
    # 중복의 경우 유연하게 처리합니다.
    i = 0
    j = 0
    find = False

    while i < len(standard_ipa):
        while i < len(standard_ipa) and (standard_ipa[i] == " " or standard_ipa[i] == "!" or standard_ipa[i] == "?" or standard_ipa[i] == "." or standard_ipa[i] == ","):
            i += 1
        if i < len(standard_ipa) and j < len(user_ipa) and standard_ipa[i] == user_ipa[j]:
            find = True
            j += 1
            while j < len(user_ipa) and (user_ipa[j] == " " or user_ipa[j] == "!" or user_ipa[j] == "?" or user_ipa[j] == "." or user_ipa[j] == ","):
                j += 1
        else:
            if find == True:
                find = False
                i += 1
            
                # 같은 문자가 나오는 동안에는 skip
                while i < len(standard_ipa) and standard_ipa[i] == standard_ipa[i-1]:
                    i += 1
            else:
                # feedback (standard[i] <-> user[j])
                # standard_array[i] 를 활용하여 standard[i] 로 교정
                arr = []
                for index, feature in enumerate(features):
                    if standard_array[i][index] != user_array[j][index]:
                        arr.append(feature)
                correction = ','.join(arr)
                feedback.append(f"{user_ipa_list[j]} 의 발음을 {correction} 를 사용해서 {standard_ipa_list[i]} 로 바꿔보세요.")
                break
    
    if not feedback:
        feedback.append("잘 하셨습니다.")
    
    return feedback

'''
# 예제
standard_ipa = 'kæt'
user_ipa = 'kʌt'

feedback = provide_feedback(standard_ipa, user_ipa)
if isinstance(feedback, str):
    print(feedback)
else:
    for fb in feedback:
        print(fb)
'''

'''
출력 결과
ʌ 의 발음을 lo 를 사용해서 æ 로 바꿔보세요.
ʌ 의 발음을 back 를 사용해서 æ 로 바꿔보세요.
'''

'''
syl: syllabic
son: sonorant
cons: consonantal
cont: continuant
delrel: delayed release
lat: lateral
nas: nasal
strid: strident
voi: voice
sg: spread glottis
cg: constricted glottis
ant: anterior
cor: coronal
distr: distributed
lab: labial
hi: high (vowel/consonant, not tone)
lo: low (vowel/consonant, not tone)
back: back
round: round
velaric: velaric airstream mechanism (click)
tense: tense
long: long

'''
