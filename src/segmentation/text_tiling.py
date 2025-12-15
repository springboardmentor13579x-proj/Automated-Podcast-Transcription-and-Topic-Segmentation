import nltk
from nltk.tokenize import TextTilingTokenizer

nltk.download("punkt")

def text_tiling_segments(text):
    
    text = text.replace(". ", ".\n\n")
    
    tokenizer = TextTilingTokenizer()
    segments = tokenizer.tokenize(text)
    return segments