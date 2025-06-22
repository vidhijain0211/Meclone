import sqlite3
import datetime
from backend.session_manager import SessionManager
from backend.memory_engine import init_memory_table, DB_PATH

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
    # Import here to avoid heavy import at module level
    from sentence_transformers import SentenceTransformer, util
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
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query, convert_to_tensor=True)
    text_embeddings = model.encode(texts, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, text_embeddings)[0]
    top_result = scores.argmax().item()
    return texts[top_result] if texts else None
