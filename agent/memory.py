import sqlite3
from pathlib import Path


class BenoitMemory:
    def __init__(self, database_path="data/benoit.db"):
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(database_path)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    def save(self, category, content):
        self.connection.execute(
            "INSERT INTO memories (category, content) VALUES (?, ?)",
            (category, content)
        )

        self.connection.commit()

        return "Mémoire sauvegardée."

    def search(self, query, limit=10):
        cursor = self.connection.execute(
            """
            SELECT category, content, created_at
            FROM memories
            WHERE content LIKE ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (f"%{query}%", limit)
        )

        results = cursor.fetchall()

        if not results:
            return "Aucune mémoire trouvée."

        output = []

        for category, content, created_at in results:
            output.append(
                f"[{category}] {created_at}\n{content}"
            )

        return "\n\n".join(output)

    def get_recent(self, limit=10):
        cursor = self.connection.execute(
            """
            SELECT category, content, created_at
            FROM memories
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()