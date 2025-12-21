import nltk
from collections import Counter
import ssl
import warnings

warnings.filterwarnings("ignore")

def setup_nlp():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

def extract_keywords(text):
    setup_nlp()
    try:
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        
        candidates = [
            w.lower() for w, t in tagged 
            if w.isalpha() and len(w) > 3 and w.lower() not in stop_words and t.startswith(('NN', 'JJ'))
        ]
        
        if not candidates:
            return "General Topic"
            
        return ", ".join([w for w, c in Counter(candidates).most_common(5)])
    except Exception:
        return "Topic"

# Only runs if you execute this file directly
if __name__ == "__main__":
    test_text = "Artificial Intelligence and Machine Learning are transforming the world."
    print(f"Keywords: {extract_keywords(test_text)}")