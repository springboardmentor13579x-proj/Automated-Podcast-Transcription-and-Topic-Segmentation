import yake

def keyword_extractor(text, top_k=8):
    extractor = yake.KeywordExtractor()
    keywords = extractor.extract_keywords(text)
    return [kw[0] for kw in keywords[:top_k]]