from rag.document_loader import DocumentLoader
from rag.splitter import get_text_splitter
from rag.vector_store import VectorStoreFactory
from services.file_service import FileService
from services.agent_service import AgentService


class IndexService:
    def __init__(self):
        self.file_service = FileService()
        self.agent_service = AgentService()
        self.loader = DocumentLoader()
        self.splitter = get_text_splitter()
        self.store_factory = VectorStoreFactory()

    def build_index(self, agent_id: str) -> dict:
        agent = self.agent_service.get_agent(agent_id)
        if not agent:
            raise ValueError("Agent不存在")

        files = self.file_service.list_unindexed_files(agent_id)
        if not files:
            return {
                "agent_id": agent_id,
                "indexed_files": 0,
                "indexed_chunks": 0,
                "status": "no_new_files",
            }

        all_docs = []
        indexed_file_ids = []

        for file_meta in files:
            docs = self.loader.load_file(file_meta["file_path"])
            split_docs = self.splitter.split_documents(docs)
            for doc in split_docs:
                doc.metadata["agent_id"] = agent_id
                doc.metadata["file_id"] = file_meta["file_id"]
                doc.metadata["file_name"] = file_meta["file_name"]
                doc.metadata["md5"] = file_meta.get("md5")
            all_docs.extend(split_docs)
            indexed_file_ids.append(file_meta["file_id"])

        if not all_docs:
            raise ValueError("没有可写入向量库的有效文本内容")

        store = self.store_factory.get_store(agent["vector_collection_name"])
        store.add_documents(all_docs)

        for file_id in indexed_file_ids:
            self.file_service.mark_indexed(agent_id, file_id)

        self.agent_service.update_agent(agent_id, knowledge_status="indexed")

        return {
            "agent_id": agent_id,
            "indexed_files": len(indexed_file_ids),
            "indexed_chunks": len(all_docs),
            "status": "success",
        }