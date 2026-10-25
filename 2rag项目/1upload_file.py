import time

import streamlit as st
from knowledge_base import KnowledgeBaseService
# 利用streamlit开发简单的网页,调用名字就可以实现
st.title("知识库更新服务")
uploader_file = st.file_uploader(
    "上传txt文件",
    type=["txt"],
    accept_multiple_files=False

)
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()
if uploader_file is not None:
    file_size = uploader_file.size / 1024  # kb
    file_name = uploader_file.name
    file_type = uploader_file.type
    st.subheader(f"文件的名字是{file_name}")
    st.write(f"文件的大小是：{file_size:.2f},类型是：{file_type}")
    # 文件中的内容
    text = uploader_file.getvalue().decode('utf-8')
    st.write(text)
    with st.spinner("知识库载入中。。。"):
        time.sleep(1)
        res = st.session_state["service"].upload_by_str(text,file_name)
        st.write(res)