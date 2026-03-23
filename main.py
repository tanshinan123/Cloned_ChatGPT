import streamlit as st

from utils import DEFAULT_PROVIDER, PROVIDER_CONFIG, get_chat_response, get_provider_settings

st.set_page_config(page_title="可乐的聊天室", page_icon="💬")

st.title("💬 可乐的聊天室")
with st.sidebar:
    provider = st.selectbox("选择模型提供方", options=list(PROVIDER_CONFIG.keys()), index=0)
    provider_settings = get_provider_settings(provider)
    openai_api_key = st.text_input(f"请输入您的 {provider} API key：", type="password")
    st.markdown(f"[获取 {provider} API key]({provider_settings['key_url']})")
    st.caption(f"默认模型：`{provider_settings['model']}`")

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
                provider=provider or DEFAULT_PROVIDER,
            )
        except Exception as e:
            response = (
                f"调用失败：{e}\n\n"
                "请检查：1) API Key 是否正确  2) 网络能否访问对应平台的 API 域名"
            )

    st.session_state["messages"].append({"role": "ai", "content": response})
    st.rerun()
