from pathlib import Path
from storage.paths import AGENTS_DIR
from storage.json_store import JsonStore
from utils.id_util import new_id
from utils.time_util import now_str


class AgentService:
    def create_agent(self, name: str, category: str, description: str, system_prompt: str) -> dict:
        agent_id = new_id()
        agent = {
            "agent_id": agent_id,
            "name": name,
            "category": category,
            "description": description,
            "system_prompt": system_prompt,
            "knowledge_status": "not_indexed",
            "created_at": now_str(),
            "updated_at": now_str(),
            "vector_collection_name": f"agent_{agent_id}",
        }
        JsonStore.save(AGENTS_DIR / f"{agent_id}.json", agent)
        return agent

    def list_agents(self) -> list[dict]:
        agents = []
        for path in AGENTS_DIR.glob("*.json"):
            agent = JsonStore.load(path, default={})
            if agent:
                agents.append(agent)
        return sorted(agents, key=lambda x: x.get("updated_at", ""), reverse=True)

    def get_agent(self, agent_id: str) -> dict | None:
        return JsonStore.load(AGENTS_DIR / f"{agent_id}.json", default=None)

    def update_agent(self, agent_id: str, **kwargs) -> dict:
        path = AGENTS_DIR / f"{agent_id}.json"
        agent = JsonStore.load(path, default=None)
        if not agent:
            raise ValueError("Agent不存在")

        agent.update(kwargs)
        agent["updated_at"] = now_str()
        JsonStore.save(path, agent)
        return agent