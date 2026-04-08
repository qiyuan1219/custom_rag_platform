from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
AGENTS_DIR = DATA_DIR / "agents"
UPLOADS_DIR = DATA_DIR / "uploads"
SESSIONS_DIR = DATA_DIR / "sessions"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
PROMPTS_DIR = BASE_DIR / "prompts"
CONFIG_DIR = BASE_DIR / "config"


def ensure_dirs() -> None:
    for path in [DATA_DIR, AGENTS_DIR, UPLOADS_DIR, SESSIONS_DIR, VECTOR_DB_DIR]:
        path.mkdir(parents=True, exist_ok=True)