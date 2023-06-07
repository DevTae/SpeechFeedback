import pandas as pd

filepath_hangul_to_ipa = "C:/Users/user/git/speech_rec_proj/ipa2Ko/IPA2Ko.csv"
filepath_standard = "C:/Users/user/git/speech_rec_proj/ipa2Ko/standard.csv"
filepath_feature = "C:/Users/user/git/speech_rec_proj/ipa2Ko/feature.csv"

def load_ipa_mapping(filepath, ipa_col, korean_col):
    df = pd.read_csv(filepath)
    return dict(zip(df[ipa_col], df[korean_col]))

def ipa_to_korean(ipa_char, ipa_dict):
    return ipa_dict.get(ipa_char)

def load_translation_mapping(filepath, eng_col, korean_col):
    df = pd.read_csv(filepath)
    return dict(zip(df[eng_col], df[korean_col]))

def translate_feature(feature, translation_dict):
    return translation_dict.get(feature)

# 예제
ipa_char = "æ" # 입력

# IPA column mapping
ipa_col = "IPA"
korean_col = "Korean"
ipa_dict = load_ipa_mapping(filepath_standard, ipa_col, korean_col)

if ipa_to_korean(ipa_char, ipa_dict) is None: # hangul_to_ipa에서 없으면 standard로
    ipa_dict = load_ipa_mapping(filepath_hangul_to_ipa, ipa_col, korean_col)

korean_char = ipa_to_korean(ipa_char, ipa_dict)
print(korean_char)  # 한국어 출력

# 예제
feature = 'cont'

# feature column mapping
eng_col = "Feature"
korean_col = "Korean"
translation_dict = load_translation_mapping(filepath_feature, eng_col, korean_col)

korean_translation = translate_feature(feature, translation_dict)
print(korean_translation)  # 한국어 연속