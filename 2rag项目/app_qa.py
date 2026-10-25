
import time
import streamlit as st
from rag import RagService
import config_data as config
st.title("智能对话")
st.divider()

# 在页面最下方提供用户输入栏
prompt = st.chat_input()
if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","message":"你好，有什么可以帮助您"}]
if "Rag" not in st.session_state:
    st.session_state["Rag"] = RagService()

for m in st.session_state["message"]:
    st.chat_message(m["role"]).write(m["message"])

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","message":prompt})
    stream_list = []

    with st.spinner("AI思考中..."):
        res_stream = st.session_state["Rag"].chain.stream({"input":prompt},config.session_config)


        def capture(generator, list):
            for chunk in generator:
                list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream,stream_list))
        st.session_state["message"].append({"role": "assistant", "message": "".join(stream_list)})