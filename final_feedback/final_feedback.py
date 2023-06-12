import pandas as pd
from panphon.featuretable import FeatureTable
import Levenshtein as lev

#### Lev similarity 사용해서 사용자 IPA와 제일 유사한 표준 IPA 반환
def most_similar_standard_ipa(user_ipa):
    # 디렉토리 내에 'standard.csv' 경로로 변경
    df = pd.read_csv('C:/Users/user/git/SpeechFeedback/final_feedback/standard.csv')
    standard_ipa_list = df['IPA'].tolist()

    # Define function to calculate similarity
    def similarity(a, b):
        return lev.ratio(a, b)
    
    # Find the most similar standard IPA
    similarities = [similarity(user_ipa, standard_ipa) for standard_ipa in standard_ipa_list]
    most_similar_index = similarities.index(max(similarities))
    most_similar_standard_ipa = standard_ipa_list[most_similar_index]

    return most_similar_standard_ipa

##### 유저 IPA와의 비교 feedback
def provide_feedback(user_ipa):
    # most_similar_standard_ipa 함수의 출력값을 표준 IPA로 사용
    standard_ipa = most_similar_standard_ipa(user_ipa)
    
    ft = FeatureTable()
    features = ['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long']
    
    if len(standard_ipa) != len(user_ipa):
        return "다시 시도하세요."
    
    standard_array = ft.word_array(features, standard_ipa)
    user_array = ft.word_array(features, user_ipa)
    
    feedback = []
    for i, (s, u) in enumerate(zip(standard_array, user_array)):
        for j, feature in enumerate(features):
          if s[j] != u[j]:
              if user_ipa[i] != standard_ipa[i]:
                  feedback.append(f"{user_ipa[i]} 의 발음을 {feature} 를 사용해서 {standard_ipa[i]} 로 바꿔보세요.")
                  korean_feature = translate_feature(feature, feature_dict)
                  feedback.append(f"{user_ipa_korean[i]} 의 발음을 {feature} 를 사용해서 {standard_ipa_korean[i]} 로 바꿔보세요.")
    
    if not feedback:
        feedback.append("잘 하셨습니다.")
    
    return feedback, standard_ipa

###### IPA to Korean
filepath_hangul_to_ipa = "C:/Users/user/git/SpeechFeedback/final_feedback/IPA2Ko.csv"
filepath_standard = "C:/Users/user/git/SpeechFeedback/final_feedback/standard.csv"
filepath_feature = "C:/Users/user/git/SpeechFeedback/final_feedback/feature.csv"

ipa_col = "IPA"
korean_col = "Korean"

def load_ipa_mapping(filepath, ipa_col, korean_col):
    df = pd.read_csv(filepath)
    return dict(zip(df[ipa_col], df[korean_col]))

def ipa_to_korean(ipa_char, ipa_dict):
    return ipa_dict.get(ipa_char)

def load_translation_mapping(filepath, eng_col, korean_col):
    df = pd.read_csv(filepath)
    return dict(zip(df[eng_col], df[korean_col]))

def load_feature_to_korean(filepath):
    df = pd.read_csv(filepath)
    return dict(zip(df["Feature"], df["Korean"]))

def translate_feature(feature, translation_dict):
    return translation_dict.get(feature)

feature_to_korean_dict = load_feature_to_korean(filepath_feature)
ipa_dict = load_ipa_mapping(filepath_standard, ipa_col, korean_col)

###### sentence 변수 선언 밑에 넣으시면 됩니다!
### 실험용 입력 
# sentence = 'ɯ'
user_ipa = sentence

if ipa_to_korean(user_ipa, ipa_dict) is None: # hangul_to_ipa에서 없으면 standard로
    ipa_dict = load_ipa_mapping(filepath_hangul_to_ipa, ipa_col, korean_col)

ipa_dict = load_ipa_mapping(filepath_hangul_to_ipa, ipa_col, korean_col)
feature_dict = load_translation_mapping(filepath_feature, 'Feature', 'Korean')

###### 여기부터 return { "reault" : sentence } 밑에 줄에 넣으시면 됩니다!
feedback, standard_ipa = provide_feedback(user_ipa)
if isinstance(feedback, str):
    print(feedback)
else:
    for fb in feedback:
        print(fb)

user_ipa_korean = ipa_to_korean(user_ipa, ipa_dict)
standard_ipa_korean = ipa_to_korean(standard_ipa, ipa_dict)