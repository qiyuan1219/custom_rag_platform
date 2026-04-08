import os
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from storage.paths import CONFIG_DIR
from utils.config_loader import ConfigLoader
model_conf = ConfigLoader.load_yaml(CONFIG_DIR / "model.yml")
def check_api_ket_set():
    """
    检查环境变量是否设置
    """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")
    return api_key
def get_chat_model():
    """
    获取百炼 Tongyi 聊天模型（LangChain 1.x 写法）
    """
    api_key = check_api_ket_set()
    return ChatTongyi(
        model_name=model_conf["chat_model_name"],
        dashscope_api_key=api_key,
        temperature=model_conf.get("temperature", 0.7),
    )

def get_embedding_model():
    """
    获取向量模型（DashScope Embedding）
    """
    api_key = check_api_ket_set()
    return DashScopeEmbeddings(
        model=model_conf["embedding_model_name"],
        dashscope_api_key=api_key,
    )


