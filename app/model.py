# app/model.py

from rake_nltk import Rake
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords")
nltk.download("punkt_tab")

# Initialize RAKE
rake = Rake()

def generate_keywords(text: str, max_phrases: int = 10) -> list: 
    """
    Extract key phrases from text using RAKE.
    """
    rake.extract_keywords_from_text(text)
    ranked_phrases = rake.get_ranked_phrases()
    return ranked_phrases[:max_phrases]
