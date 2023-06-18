import pandas as pd

filepath_ipa_to_hangul = "csv/ipa2ko.csv"
filepath_standard = "csv/standard.csv"
filepath_feature = "csv/feature.csv"

feature_col = "Feature"
ipa_col = "IPA"
korean_col = "Korean"

def load_ipa_mapping(filepath, ipa_col, korean_col):
    df = pd.read_csv(filepath)
    return dict(zip(df[ipa_col], df[korean_col]))

def ipa_to_hangul(ipa_char, ipa_dict):
    return ipa_dict.get(ipa_char)

def load_translation_mapping(filepath, eng_col, korean_col):
    df = pd.read_csv(filepath)
    return dict(zip(df[eng_col], df[korean_col]))

def translate_feature(feature, translation_dict):
    return translation_dict.get(feature)

def get_info_of_ipa(ipa_char : str = "æ", feature : str = 'cont'):
    # IPA column mapping
    ipa_col = "IPA"
    hangul_col = "Korean"
    ipa_dict = load_ipa_mapping(filepath_standard, ipa_col, hangul_col)

    if ipa_to_hangul(ipa_char, ipa_dict) is None: # filepath_ipa_to_hangul 에서 없으면 standard 로
        ipa_dict = load_ipa_mapping(filepath_ipa_to_hangul, ipa_col, hangul_col)
    
    hangul_char = ipa_to_hangul(ipa_char, ipa_dict)
    
    # feature column mapping
    eng_col = "Feature"
    hangul_col = "Korean"
    translation_dict = load_translation_mapping(filepath_feature, eng_col, hangul_col)
    
    hangul_translation = translate_feature(feature, translation_dict)

    #print(hangul_char)  # 한국어 출력
    #print(hangul_translation)  # 한국어 연속

    return hangul_char, hangul_translation

ipa_dict = load_ipa_mapping(filepath_ipa_to_hangul, ipa_col, korean_col)
feature_dict = load_translation_mapping(filepath_feature, feature_col, korean_col)



