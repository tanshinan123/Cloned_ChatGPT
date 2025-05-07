import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import get_chat_response

st.title("💬可乐的聊天室")
with st.sidebar:
    openai_api_key = st.text_input("请输入您的OpenAI API key：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/api-key)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{
        "role": "ai",
        "content": "你好，我是你的专属AI助手可乐，你有什么想和我聊的吗？"
    }]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("您想聊些什么呢")
if prompt:
    if not openai_api_key:
        st.info("您忘记输入Open API Key啦")
        st.stop()
    st.session_state["messages"].append({
        "role": "human",
        "content": prompt
    })
    st.chat_message("human").write(prompt)

    with st.spinner("对方正在输入中..."):
        response = get_chat_response(prompt, st.session_state["memory"], openai_api_key)
    message_list = {"role": "ai", "content": response}
    st.session_state["messages"].append(message_list)
    st.chat_message("ai").write(response)