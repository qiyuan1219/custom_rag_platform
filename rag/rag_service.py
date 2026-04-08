from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model.factory import get_chat_model
from rag.vector_store import VectorStoreFactory
from services.agent_service import AgentService
from storage.paths import PROMPTS_DIR, CONFIG_DIR
from utils.config_loader import ConfigLoader


rag_conf = ConfigLoader.load_yaml(CONFIG_DIR / "rag.yml")


def format_docs(docs) -> str:
    blocks = []
    for doc in docs:
        source = doc.metadata.get("source", doc.metadata.get("file_name", "未知来源"))
        page = doc.metadata.get("page")
        title = f"来源：{source}" if not page else f"来源：{source} 第{page}页"
        blocks.append(f"【{title}】{doc.page_content}")
    return "".join(blocks)


class RagService:
    def __init__(self):
        self.model = get_chat_model()
        self.agent_service = AgentService()
        self.store_factory = VectorStoreFactory()
        self.rag_template = (PROMPTS_DIR / "rag_qa_prompt.txt").read_text(encoding="utf-8")

    def ask(self, agent_id: str, question: str) -> dict:
        agent = self.agent_service.get_agent(agent_id)
        if not agent:
            raise ValueError("Agent不存在")

        store = self.store_factory.get_store(agent["vector_collection_name"])
        retriever = store.as_retriever(search_kwargs={"k": rag_conf["search_k"]})
        docs = retriever.invoke(question)
        context = format_docs(docs)

        prompt = PromptTemplate.from_template(self.rag_template)
        chain = prompt | self.model | StrOutputParser()
        answer = chain.invoke({
            "agent_name": agent["name"],
            "system_prompt": agent["system_prompt"],
            "context": context,
            "question": question,
        })

        references = []
        for doc in docs:
            references.append({
                "file_name": doc.metadata.get("file_name", doc.metadata.get("source", "未知来源")),
                "page": doc.metadata.get("page"),
                "preview": doc.page_content[:220],
            })

        return {
            "answer": answer,
            "references": references,
            "hit_count": len(docs),
        }