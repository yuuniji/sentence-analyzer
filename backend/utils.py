# utils.py
import re
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
    增加短句容错：若文本中英文字母占比较高，则视为英文，避免 langdetect 误判。
    """
    # 移除空白字符和常见标点后，统计纯英文字母的比例
    clean_text = re.sub(r'[\s\d.,;:!?\'"()\[\]{}-]', '', text)
    if not clean_text:
        return "en"
        
    letters = re.findall(r'[a-zA-Z]', clean_text)
    if len(letters) / len(clean_text) > 0.5:
        return "en"
        
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "en"
