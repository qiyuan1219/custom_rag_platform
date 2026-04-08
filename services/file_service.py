import hashlib
from pathlib import Path

from storage.paths import UPLOADS_DIR
from utils.time_util import now_str
from utils.id_util import new_id
from storage.json_store import JsonStore


class FileService:
    @staticmethod
    def _calc_md5_bytes(content: bytes) -> str:
        return hashlib.md5(content).hexdigest()

    def save_uploaded_file(self, agent_id: str, uploaded_file) -> dict:
        agent_dir = UPLOADS_DIR / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)

        content = uploaded_file.getbuffer().tobytes()
        file_md5 = self._calc_md5_bytes(content)

        for meta in self.list_files(agent_id):
            if meta.get("md5") == file_md5 and meta.get("file_name") == uploaded_file.name:
                return meta

        file_id = new_id()
        file_path = agent_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(content)

        meta = {
            "file_id": file_id,
            "agent_id": agent_id,
            "file_name": uploaded_file.name,
            "file_path": str(file_path),
            "upload_time": now_str(),
            "status": "uploaded",
            "md5": file_md5,
            "indexed_at": None,
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

    def list_unindexed_files(self, agent_id: str) -> list[dict]:
        return [f for f in self.list_files(agent_id) if f.get("status") != "indexed"]

    def get_file_meta(self, agent_id: str, file_id: str) -> dict | None:
        meta_path = UPLOADS_DIR / agent_id / f"{file_id}.meta.json"
        return JsonStore.load(meta_path, default=None)

    def mark_indexed(self, agent_id: str, file_id: str) -> None:
        meta_path = UPLOADS_DIR / agent_id / f"{file_id}.meta.json"
        meta = JsonStore.load(meta_path, default=None)
        if not meta:
            return

        meta["status"] = "indexed"
        meta["indexed_at"] = now_str()
        JsonStore.save(meta_path, meta)

    def mark_uploaded(self, agent_id: str, file_id: str) -> None:
        meta_path = UPLOADS_DIR / agent_id / f"{file_id}.meta.json"
        meta = JsonStore.load(meta_path, default=None)
        if not meta:
            return

        meta["status"] = "uploaded"
        meta["indexed_at"] = None
        JsonStore.save(meta_path, meta)

    def delete_file(self, agent_id: str, file_id: str) -> None:
        """
        只删除源文件和元数据，不处理向量。
        向量删除交给上层索引服务处理。
        """
        meta_path = UPLOADS_DIR / agent_id / f"{file_id}.meta.json"
        meta = JsonStore.load(meta_path, default=None)
        if not meta:
            return

        file_path = Path(meta["file_path"])
        if file_path.exists():
            file_path.unlink()

        if meta_path.exists():
            meta_path.unlink()