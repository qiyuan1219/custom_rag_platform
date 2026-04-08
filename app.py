import streamlit as st
from storage.paths import ensure_dirs
from ui.components.sidebar import render_sidebar
from ui.pages.agent_manage import render_agent_manage_page
from ui.pages.knowledge_manage import render_knowledge_manage_page
from ui.pages.chat_page import render_chat_page
import uuid


def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_kb" not in st.session_state:
        st.session_state.current_kb = None

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "show_create_agent_form" not in st.session_state:
        st.session_state.show_create_agent_form = False


def main():
    init_session_state()
    ensure_dirs()
    st.set_page_config(page_title="Custom RAG Platform", layout="wide")
    st.title("Custom RAG Platform")
    st.caption("支持多 Agent、自定义 Prompt、上传资料、手动向量化与按领域问答")

    selected_agent_id, action = render_sidebar()

    if action == "create":
        st.session_state.show_create_agent_form = True
    elif action == "delete":
        st.session_state.show_create_agent_form = False

    tab1, tab2, tab3 = st.tabs(["Agent管理", "知识库管理", "聊天问答"])

    with tab1:
        render_agent_manage_page(selected_agent_id)

    with tab2:
        render_knowledge_manage_page(selected_agent_id)

    with tab3:
        render_chat_page(selected_agent_id)


if __name__ == "__main__":
    main()