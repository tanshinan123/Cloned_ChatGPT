import streamlit as st

from utils import get_chat_response

st.set_page_config(page_title="可乐的聊天室", page_icon="💬")

st.title("💬 可乐的聊天室")
with st.sidebar:
    openai_api_key = st.text_input("请输入您的 DeepSeek API key：", type="password")
    st.markdown("[获取 DeepSeek API key](https://platform.deepseek.com)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "ai",
            "content": "你好，我是你的专属AI助手可乐，你有什么想和我聊的吗？",
        }
    ]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("您想聊些什么呢")
if prompt:
    if not openai_api_key or not openai_api_key.strip():
        st.info("您忘记输入 DeepSeek API Key 啦")
        st.stop()

    st.session_state["messages"].append({"role": "human", "content": prompt})

    with st.spinner("对方正在输入中..."):
        try:
            response = get_chat_response(
                openai_api_key.strip(),
                st.session_state["messages"],
            )
        except Exception as e:
            response = (
                f"调用失败：{e}\n\n"
                "请检查：1) API Key 是否正确  2) 网络能否访问 api.deepseek.com"
            )

    st.session_state["messages"].append({"role": "ai", "content": response})
    st.rerun()
