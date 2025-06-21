import json
import os
import datetime
from sentence_transformers import SentenceTransformer, util
DATA_FILE = "data/reflections.json"
model = SentenceTransformer('all-MiniLM-L6-v2')

def save_reflection(text):
    thoughts = load_reflections()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thoughts.append({"text": text, "timestamp": timestamp})
    save_reflections(thoughts)


def load_reflections():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_reflections(thoughts):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as file:
        json.dump(thoughts, file, indent=4)


def get_all_reflections():
    thoughts = load_reflections()
    return [(t["text"], t["timestamp"]) for t in thoughts]


def delete_reflection(text):
    thoughts = load_reflections()
    thoughts = [t for t in thoughts if t["text"] != text]
    save_reflections(thoughts)


def get_relevant_reflection(query, top_k=1):
    try:
        with open(DATA_FILE, "r") as f:
            thoughts = json.load(f)
    except:
        return None

    if not thoughts:
        return None

    # Extract only text part for comparison
    texts = [t["text"] for t in thoughts]

    # Get embeddings
    query_embedding = model.encode(query, convert_to_tensor=True)
    text_embeddings = model.encode(texts, convert_to_tensor=True)

    # Compute similarity scores
    scores = util.pytorch_cos_sim(query_embedding, text_embeddings)[0]
    top_result = scores.argmax().item()

    return texts[top_result]  # ✅ only return the text (no time)
