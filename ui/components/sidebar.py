import streamlit as st
from services.agent_service import AgentService


def render_sidebar():
    st.sidebar.title("Agent 列表")
    service = AgentService()
    agents = service.list_agents()

    action = None

    if not agents:
        st.sidebar.info("还没有Agent，请先创建。")
        if st.sidebar.button("新建 Agent", use_container_width=True):
            action = "create"
        return None, action

    options = {f"{a['name']}（{a['category']}）": a["agent_id"] for a in agents}
    selected_label = st.sidebar.selectbox("选择当前Agent", list(options.keys()))
    selected_agent_id = options[selected_label]

    st.sidebar.markdown("---")

    # ✅ 新建按钮
    if st.sidebar.button("新建 Agent", use_container_width=True):
        action = "create"

    # ✅ 删除按钮
    if st.sidebar.button("删除当前 Agent", use_container_width=True):
        service.delete_agent(selected_agent_id)
        st.sidebar.success("删除成功")
        action = "delete"
        st.rerun()

    return selected_agent_id, action