import pandas as pd
import streamlit as st
from services.file_service import FileService
from rag.index_service import IndexService


def render_knowledge_manage_page(agent_id: str):
    st.header("知识库管理")
    if not agent_id:
        st.info("请先在左侧选择或创建 Agent")
        return

    file_service = FileService()
    index_service = IndexService()

    uploaded_files = st.file_uploader(
        "上传参考资料",
        type=["txt", "md", "pdf", "docx"],
        accept_multiple_files=True,
    )

    if uploaded_files and st.button("保存上传资料"):
        count = 0
        for uploaded_file in uploaded_files:
            file_service.save_uploaded_file(agent_id, uploaded_file)
            count += 1
        st.success(f"已处理 {count} 个文件；重复文件会自动跳过")

    files = file_service.list_files(agent_id)
    st.subheader("当前资料")
    if not files:
        st.write("暂无资料")
    else:
        show_df = pd.DataFrame([
            {
                "file_id": f["file_id"],
                "文件名": f["file_name"],
                "状态": f["status"],
                "上传时间": f["upload_time"],
                "索引时间": f.get("indexed_at"),
            }
            for f in files
        ])
        st.dataframe(show_df, use_container_width=True)

        delete_file_id = st.selectbox(
            "选择要删除的文件",
            options=[""] + [f["file_id"] for f in files],
            format_func=lambda x: "请选择文件" if x == "" else next(i["file_name"] for i in files if i["file_id"] == x),
        )
        if delete_file_id and st.button("删除选中文件"):
            file_service.delete_file(agent_id, delete_file_id)
            st.success("文件已删除，请手动重新向量化以更新知识库")
            st.rerun()

    if st.button("开始向量化"):
        try:
            result = index_service.build_index(agent_id)
            if result["status"] == "no_new_files":
                st.info("没有新的未索引文件")
            else:
                st.success(
                    f"向量化完成：新增文件数 {result['indexed_files']}，新增切片数 {result['indexed_chunks']}"
                )
        except Exception as e:
            st.error(str(e))