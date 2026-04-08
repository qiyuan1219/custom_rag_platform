from rag.rag_service import RagService
from services.session_service import SessionService


class ChatService:
    def __init__(self):
        self.rag_service = RagService()
        self.session_service = SessionService()

    def chat(self, agent_id: str, session_id: str, question: str) -> dict:
        self.session_service.append_message(session_id, "user", question)
        result = self.rag_service.ask(agent_id, question)
        self.session_service.append_message(session_id, "assistant", result["answer"])
        return result