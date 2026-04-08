import streamlit as st
from services.agent_service import AgentService
from ui.components.prompt_editor import PromptEditor


DEFAULT_PROMPTS = {
    "diet": "你是一名专业的饮食顾问。",
    "health": "你是一名健康知识助手。",
    "education": "你是一名教育学习助手。",
    "custom": "你是一名可自定义的智能助手。",
}


def render_agent_manage_page(selected_agent_id: str | None = None):
    st.header("Agent 管理")
    service = AgentService()
    prompt_editor = PromptEditor()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.session_state.get("show_create_agent_form", False):
            with st.form("create_agent_form"):
                name = st.text_input("Agent 名称")
                category = st.selectbox("Agent 类型", ["diet", "health", "education", "custom"])
                description = st.text_area("描述")
                system_prompt = st.text_area("系统 Prompt", value=DEFAULT_PROMPTS[category], height=220)
                submitted = st.form_submit_button("创建 Agent")

                if submitted:
                    if not name.strip():
                        st.error("Agent 名称不能为空")
                    else:
                        agent = service.create_agent(
                            name=name.strip(),
                            category=category,
                            description=description.strip(),
                            system_prompt=system_prompt.strip(),
                        )
                        st.session_state.show_create_agent_form = False
                        st.success(f"创建成功：{agent['name']}")
                        st.rerun()
        else:
            st.info("左侧点击“新建 Agent”后，在这里填写创建信息。")

    with col2:
        if selected_agent_id:
            prompt_editor.render(selected_agent_id)
        else:
            st.info("左侧选择一个 Agent 后，可以在这里编辑 Prompt。")