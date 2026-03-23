# -*- coding: utf-8 -*-
"""
可乐聊天室 — DeepSeek 接入（OpenAI 兼容 SDK，与 lingjing 一致，避免 langchain_openai + Pydantic v2 冲突）
"""

from __future__ import annotations

from typing import Any

from openai import OpenAI

PROVIDER_CONFIG: dict[str, dict[str, str]] = {
    "DeepSeek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "key_url": "https://platform.deepseek.com",
    },
    "通义百炼": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "key_url": "https://bailian.console.aliyun.com/",
    },
    "Kimi": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
        "key_url": "https://platform.moonshot.cn/console/api-keys",
    },
}

DEFAULT_PROVIDER = "DeepSeek"

SYSTEM_PROMPT = (
    "你是「可乐」，一位友好、幽默、耐心的中文 AI 助手。"
    "回复简洁自然，适当使用 emoji；不要编造事实。"
)


def _streamlit_messages_to_openai(chat_messages: list[dict[str, Any]]) -> list[dict[str, str]]:
    """将 main.py 中的 role: human/ai 转为 OpenAI 的 user/assistant。"""
    out: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in chat_messages:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if not content:
            continue
        if role == "human":
            out.append({"role": "user", "content": content})
        elif role == "ai":
            out.append({"role": "assistant", "content": content})
    return out


def get_provider_settings(provider: str) -> dict[str, str]:
    """获取不同提供方的默认配置，未知值回退到 DeepSeek。"""
    return PROVIDER_CONFIG.get(provider, PROVIDER_CONFIG[DEFAULT_PROVIDER])


def get_chat_response(
    api_key: str,
    chat_messages: list[dict[str, Any]],
    *,
    provider: str = DEFAULT_PROVIDER,
    model: str | None = None,
    base_url: str | None = None,
) -> str:
    """
    根据当前会话消息列表调用 DeepSeek，返回助手回复。
    chat_messages 须已包含本轮用户的最后一条 human 消息（与 main.py 逻辑一致）。
    """
    settings = get_provider_settings(provider)
    final_base_url = (base_url or settings["base_url"]).strip()
    final_model = (model or settings["model"]).strip()

    client = OpenAI(api_key=api_key.strip(), base_url=final_base_url)
    messages = _streamlit_messages_to_openai(chat_messages)
    if len(messages) <= 1:
        return "（没有有效的用户消息，请重新输入。）"

    resp = client.chat.completions.create(
        model=final_model,
        messages=messages,
        temperature=0.7,
    )
    choice = resp.choices[0]
    text = (choice.message.content or "").strip()
    return text if text else "（模型返回为空，请重试。）"
