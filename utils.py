import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="gpt-4-turbo",
                       openai_api_key=openai_api_key,
                       base_url="https://api.aigc369.com/v1")
    chain = ConversationChain(llm=model, memory=memory)
    response = chain.invoke({"input": prompt})
    return response["response"]


# memory = ConversationBufferMemory(return_messages=True)
# print(get_chat_response("你好我的名字是可乐", memory, os.getenv("OPENAI_API_KEY")))
# print(get_chat_response("我的上一个问题是什么", memory, os.getenv("OPENAI_API_KEY")))
