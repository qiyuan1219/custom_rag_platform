import streamlit as st
from services.agent_service import AgentService


class PromptEditor:
    def __init__(self):
        self.agent_service = AgentService()

    def render(self, agent_id: str) -> None:
        if not agent_id:
            st.info("请先选择一个 Agent")
            return

        agent = self.agent_service.get_agent(agent_id)
        if not agent:
            st.error("Agent不存在")
            return

        st.subheader("Prompt 编辑")
        prompt_value = st.text_area(
            "系统 Prompt",
            value=agent.get("system_prompt", ""),
            height=240,
            key=f"prompt_editor_{agent_id}",
        )

        if st.button("保存 Prompt", key=f"save_prompt_{agent_id}"):
            self.agent_service.update_agent(agent_id, system_prompt=prompt_value)
            st.success("Prompt 已保存")