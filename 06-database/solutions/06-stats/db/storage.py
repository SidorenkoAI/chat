import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "chat.db"


def get_connection() -> sqlite3.Connection:
    # check_same_thread=False: соединением пользуются потоки разных клиентов.
    # За то, чтобы два потока не писали одновременно, отвечает ChatServer.lock.
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    return conn


def save_message(conn: sqlite3.Connection, from_user: str, text: str) -> None:
    conn.execute("INSERT INTO messages (from_user, text) VALUES (?, ?)", (from_user, text))
    conn.commit()


def load_history(conn: sqlite3.Connection, limit: int) -> list[tuple[str, str, str]]:
    rows = conn.execute(
        "SELECT from_user, text, created_at FROM messages ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return list(reversed(rows))


def top_senders(conn: sqlite3.Connection, limit: int = 3) -> list[tuple[str, int]]:
    return conn.execute(
        "SELECT from_user, COUNT(*) AS cnt FROM messages "
        "GROUP BY from_user ORDER BY cnt DESC LIMIT ?",
        (limit,),
    ).fetchall()
