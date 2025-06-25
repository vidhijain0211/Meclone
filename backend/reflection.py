import sqlite3
import datetime
from backend.session_manager import SessionManager
from backend.memory_engine import init_memory_table, DB_PATH

_model_cache = None

def get_sentence_transformer():
    global _model_cache
    if _model_cache is None:
        from sentence_transformers import SentenceTransformer
        _model_cache = SentenceTransformer('all-MiniLM-L6-v2')
    return _model_cache

def save_reflection(text, user_id=None):
    if user_id is None:
        user_id = SessionManager().get_logged_in_user()
    if not user_id:
        return
    init_memory_table()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO thoughts (user_id, timestamp, content) VALUES (?, ?, ?)", (user_id, timestamp, text))
        conn.commit()


def get_all_reflections(user_id=None):
    if user_id is None:
        user_id = SessionManager().get_logged_in_user()
    if not user_id:
        return []
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT content, timestamp FROM thoughts WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        return c.fetchall()


def delete_reflection(text, user_id=None):
    if user_id is None:
        user_id = SessionManager().get_logged_in_user()
    if not user_id:
        return
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM thoughts WHERE user_id = ? AND content = ?", (user_id, text))
        conn.commit()


def get_relevant_reflection(query, user_id=None, top_k=1):
    from sentence_transformers import util
    if user_id is None:
        user_id = SessionManager().get_logged_in_user()
    if not user_id:
        return None
    init_memory_table()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT content FROM thoughts WHERE user_id = ?", (user_id,))
        rows = c.fetchall()
        if not rows:
            return None
        texts = [row[0] for row in rows]
    model = get_sentence_transformer()
    query_embedding = model.encode(query, convert_to_tensor=True)
    text_embeddings = model.encode(texts, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, text_embeddings)[0]
    top_result = scores.argmax().item()
    top_score = float(scores[top_result])
    if top_score < 0.3:
        return "Sorry, no relevant reflection found."
    return texts[top_result] if texts else None
