#pip install panphon

from panphon.featuretable import FeatureTable

def provide_feedback(standard_ipa, user_ipa):
    ft = FeatureTable()
    features = ['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    
    standard_ipa_list = list(standard_ipa)
    user_ipa_list = list(user_ipa)
    
    if len(standard_ipa_list) != len(user_ipa_list):
        return "다시 시도하세요."
    
    standard_array = ft.word_array(features, standard_ipa)
    user_array = ft.word_array(features, user_ipa)
    
    feedback = []
    for i, (s, u) in enumerate(zip(standard_array, user_array)):
        for j, feature in enumerate(features):
          if s[j] != u[j]:
              if user_ipa_list[i] != standard_ipa_list[i]:
                  feedback.append(f"{user_ipa_list[i]} 의 발음을 {feature} 를 사용해서 {standard_ipa_list[i]} 로 바꿔보세요.")
    
    if not feedback:
        feedback.append("잘 하셨습니다.")
    
    return feedback

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
