from flask import Flask, request, jsonify
from flask_cors import CORS
import random, re
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet")
nltk.download("omw-1.4")

app = Flask(__name__)
CORS(app)  # <-- allow JS to call backend

def get_synonym(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ")
            if synonym.lower() != word.lower():
                synonyms.append(synonym)
    return random.choice(synonyms) if synonyms else word

def humanize_text(text, synonym_chance=0.3):
    sentences = re.split(r'(?<=[.!?]) +', text)
    new_sentences = []

    for sentence in sentences:
        words = sentence.split()
        new_words = []
        for word in words:
            stripped = re.sub(r'[^\w\s]', '', word)
            if stripped.isalpha() and random.random() < synonym_chance:
                new_word = get_synonym(stripped)
                if word[0].isupper():
                    new_word = new_word.capitalize()
                if word[-1] in ",.!?":
                    new_word += word[-1]
                new_words.append(new_word)
            else:
                new_words.append(word)
        new_sentences.append(" ".join(new_words))

    return " ".join(new_sentences)

@app.route("/humanize", methods=["POST"])
def humanize_api():
    data = request.get_json()
    text = data.get("text", "")
    return jsonify({"humanized_text": humanize_text(text)})

if __name__ == "__main__":
    app.run(debug=True)
