import spacy
from transformations.dat.colors import get_color_mapping
nlp = spacy.load("en_core_web_sm")

def segment_text(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


def highlight(story, highlight_schema):
    segments = segment_text(story)
    original_text = story
    print(segments)
    for segment in segments:
        print(segment)
        print("-----")