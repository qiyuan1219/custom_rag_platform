from pathlib import Path
from storage.paths import UPLOADS_DIR
from utils.time_util import now_str
from utils.id_util import new_id
from storage.json_store import JsonStore


class FileService:
    def save_uploaded_file(self, agent_id: str, uploaded_file) -> dict:
        agent_dir = UPLOADS_DIR / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)

        file_id = new_id()
        file_path = agent_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        meta = {
            "file_id": file_id,
            "agent_id": agent_id,
            "file_name": uploaded_file.name,
            "file_path": str(file_path),
            "upload_time": now_str(),
            "status": "uploaded",
        }
        JsonStore.save(agent_dir / f"{file_id}.meta.json", meta)
        return meta

    def list_files(self, agent_id: str) -> list[dict]:
        agent_dir = UPLOADS_DIR / agent_id
        if not agent_dir.exists():
            return []
        result = []
        for path in agent_dir.glob("*.meta.json"):
            meta = JsonStore.load(path, default={})
            if meta:
                result.append(meta)
        return sorted(result, key=lambda x: x.get("upload_time", ""), reverse=True)