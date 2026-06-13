# utils.py
from langdetect import detect, LangDetectException

def extract_trunk(sentence: str) -> str:
    """
    策略：取句子前 80 个字符，在最近的逗号/分号处截断，
    追加省略号。若句子本身较短则直接使用原句。
    """
    if len(sentence) <= 100:
        return sentence
    
    trunk = sentence[:80]
    # 在最近的标点处断开
    for punct in [',', ';', ' and ', ' or ', ' but ']:
        idx = trunk.rfind(punct)
        if idx > 40:
            return trunk[:idx] + '...'
    
    return trunk[:75] + '...'

def detect_language(text: str) -> str:
    """
    检测文本语言，返回小写的语言代码，如 'en', 'zh-cn' 等。
    如果检测失败，默认返回 'en' (容错)。
    """
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "en"
