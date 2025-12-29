import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DB_PATH = os.path.join(BASE_DIR, "labguard.db")

API_KEY = "LAB02_INGEST_2e7c91aaf3b84d10"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
INSERT OR IGNORE INTO sdk_keys (lab_id, sdk_id, api_key, active)
VALUES (?, ?, ?, 1)
""", (
    "LAB-02",
    "SDK-LAB-02",
    API_KEY
))

conn.commit()
conn.close()

print("✅ SDK key seeded")
