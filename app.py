from flask import Flask, request, jsonify
from flask_cors import CORS
import random, re
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download required NLTK data
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

import language_tool_python

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

# ----------------- Synonym Utilities -----------------
def get_synonym(word, pos_tag=None):
    synonyms = []
    for syn in wordnet.synsets(word):
        if pos_tag and syn.pos() != pos_tag:
            continue
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ")
            if synonym.lower() != word.lower() and " " not in synonym and synonym.isalpha():
                synonyms.append(synonym)
    return random.choice(synonyms) if synonyms else word

def nltk_pos_to_wordnet(tag):
    if tag.startswith("J"):
        return "a"
    elif tag.startswith("V"):
        return "v"
    elif tag.startswith("N"):
        return "n"
    elif tag.startswith("R"):
        return "r"
    else:
        return None

# ----------------- Grammar Utilities -----------------
import language_tool_python

def init_language_tool():
    try:
        # Default constructor, no java_options / small args
        tool_local = language_tool_python.LanguageTool("en-US")
        return tool_local
    except Exception as e:
        print("Error initializing LanguageTool:", e)
        return None

# Initialize tool
tool = init_language_tool()


def grammar_fix(text):
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    return corrected

# ----------------- Text Humanizer -----------------
def humanize_text(text, synonym_chance=0.1):
    sentences = re.split(r'(?<=[.!?]) +', text)
    new_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        new_words = []
        for (word, tag) in tagged:
            stripped = re.sub(r"[^\w\s]", "", word)
            if stripped.isalpha() and random.random() < synonym_chance:
                wn_tag = nltk_pos_to_wordnet(tag)
                if wn_tag:
                    new_word = get_synonym(stripped, wn_tag)
                    if word[0].isupper():
                        new_word = new_word.capitalize()
                    if word[-1] in ",.!?":
                        new_word += word[-1]
                    new_words.append(new_word)
                    continue
            new_words.append(word)
        new_sentences.append(" ".join(new_words))
    final_text = " ".join(new_sentences)
    return grammar_fix(final_text)

# ----------------- Flask API -----------------
@app.route("/humanize", methods=["POST"])
def humanize_api():
    data = request.get_json()
    text = data.get("text", "")
    humanized = humanize_text(text)
    return jsonify({"humanized_text": humanized})

if __name__ == "__main__":
    app.run(debug=True)
