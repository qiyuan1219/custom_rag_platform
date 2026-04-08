from storage.paths import SESSIONS_DIR
from storage.json_store import JsonStore
from utils.id_util import new_id
from utils.time_util import now_str


class SessionService:
    def create_session(self, agent_id: str, title: str = "新会话") -> dict:
        session_id = new_id()
        session = {
            "session_id": session_id,
            "agent_id": agent_id,
            "title": title,
            "created_at": now_str(),
            "updated_at": now_str(),
            "messages": [],
        }
        JsonStore.save(SESSIONS_DIR / f"{session_id}.json", session)
        return session

    def get_session(self, session_id: str) -> dict | None:
        return JsonStore.load(SESSIONS_DIR / f"{session_id}.json", default=None)

    def append_message(self, session_id: str, role: str, content: str) -> dict:
        path = SESSIONS_DIR / f"{session_id}.json"
        session = JsonStore.load(path, default=None)
        if not session:
            raise ValueError("会话不存在")

        session["messages"].append({
            "role": role,
            "content": content,
            "created_at": now_str(),
        })
        session["updated_at"] = now_str()
        JsonStore.save(path, session)
        return session