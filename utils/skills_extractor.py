import spacy

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    """
    Extracts skills from text using NLP.

    Args:
        text (str): Input text (resume or job description)

    Returns:
        set: A set of extracted skills
    """
    doc = nlp(text.lower())  # Convert text to lowercase for consistency
    skills = {token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2}
    
    return skills if skills else set()
