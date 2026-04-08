import streamlit as st
from services.session_service import SessionService
from services.chat_service import ChatService


def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "current_agent_id" not in st.session_state:
        st.session_state.current_agent_id = None


def render_chat_page(agent_id: str):
    st.header("聊天问答")
    if not agent_id:
        st.info("请先选择一个 Agent")
        return

    init_session_state()
    session_service = SessionService()
    chat_service = ChatService()

    # Agent切换时，自动切换到新会话
    if st.session_state.current_agent_id != agent_id or not st.session_state.session_id:
        session = session_service.create_session(agent_id)
        st.session_state.session_id = session["session_id"]
        st.session_state.current_agent_id = agent_id
        st.rerun()

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("新建会话", use_container_width=True):
            session = session_service.create_session(agent_id)
            st.session_state.session_id = session["session_id"]
            st.rerun()

    with col2:
        if st.button("清空对话", use_container_width=True):
            session = session_service.create_session(agent_id)
            st.session_state.session_id = session["session_id"]
            st.rerun()

    session = session_service.get_session(st.session_state.session_id)
    for message in session["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    response_container = st.container()

    question = st.chat_input("请输入你的问题")
    if question:
        with response_container:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    result = chat_service.chat(agent_id, st.session_state.session_id, question)
                    st.write(result["answer"])
                    with st.expander(f"参考资料（命中 {result['hit_count']} 条）"):
                        for idx, ref in enumerate(result["references"], start=1):
                            page_text = f" | 第{ref['page']}页" if ref.get("page") else ""
                            st.markdown(f"**{idx}. {ref['file_name']}**{page_text}")
                            st.caption(ref["preview"])