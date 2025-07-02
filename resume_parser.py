import random
from textblob import TextBlob
import docx2txt
import PyPDF2
import os

# Extract text from .pdf
def extract_text_from_pdf(path):
    text = ""
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except:
        pass
    return text

# Extract text from .docx
def extract_text_from_docx(path):
    try:
        return docx2txt.process(path)
    except:
        return ""

# Universal text extractor
def extract_text(path):
    if path.endswith('.pdf'):
        return extract_text_from_pdf(path)
    elif path.endswith('.docx'):
        return extract_text_from_docx(path)
    else:
        return ""

# Simulate resume scoring, sentiment & keyword detection
def parse_resume(file_path):
    text = extract_text(file_path)
    blob = TextBlob(text)

    sentiment = "Positive" if blob.sentiment.polarity > 0 else (
        "Negative" if blob.sentiment.polarity < 0 else "Neutral"
    )

    # Dummy keyword check
    keywords = []
    required_keywords = ['Python', 'Machine Learning', 'SQL', 'AWS', 'Docker', 'JavaScript']
    for word in required_keywords:
        if word.lower() in text.lower():
            keywords.append(word)

    # Score based on keywords found
    score = int((len(keywords) / len(required_keywords)) * 100)

    return score, sentiment, keywords
