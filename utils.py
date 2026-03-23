# -*- coding: utf-8 -*-
"""
可乐聊天室 — DeepSeek 接入（OpenAI 兼容 SDK，与 lingjing 一致，避免 langchain_openai + Pydantic v2 冲突）
"""

from __future__ import annotations

from typing import Any

from openai import OpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"

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


def get_chat_response(
    api_key: str,
    chat_messages: list[dict[str, Any]],
    *,
    model: str = DEFAULT_MODEL,
    base_url: str = DEEPSEEK_BASE_URL,
) -> str:
    """
    根据当前会话消息列表调用 DeepSeek，返回助手回复。
    chat_messages 须已包含本轮用户的最后一条 human 消息（与 main.py 逻辑一致）。
    """
    client = OpenAI(api_key=api_key.strip(), base_url=base_url)
    messages = _streamlit_messages_to_openai(chat_messages)
    if len(messages) <= 1:
        return "（没有有效的用户消息，请重新输入。）"

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    choice = resp.choices[0]
    text = (choice.message.content or "").strip()
    return text if text else "（模型返回为空，请重试。）"
