import streamlit as st  # 导入Streamlit库
from openai import OpenAI  # 导入OpenAI库

# 定义一个函数，用于与deepseek API交互，获取AI的回复
def ai(prompt):
    r = ''
    # 创建一个deepseek客户端实例
    client = OpenAI(api_key="sk-a018798f114c42b783fdf8c2760f49e2", base_url="https://api.deepseek.com")
    
    # 发送一个请求到deepseek API，获取AI的回复
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是由万载智酷机器人开发的人工智能助手,请你在介绍自己的时候用这个身份"},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    # 获取聊天界面的AI消息部分
    ai_chat = st.chat_message("AI")
    ai_empty = ai_chat.empty()
    # 逐个处理API返回的回复
    for i in response:
        r += i.choices[0].delta.content
        ai_empty.write(r)
    return r

# 设置Streamlit页面的配置
st.set_page_config(page_title="智酷AI助手", layout="wide", page_icon="🤖")
# 设置页面标题
st.title("智酷AI助手")

# 初始化session_state中的prompt和history
if "prompt" not in st.session_state:
    st.session_state["prompt"] = []
if 'history' not in st.session_state:
    st.session_state["history"] = ''
    ai("你是谁?")

# 获取用户输入的聊天消息
prompt = st.chat_input("请输入问题")
# 输出历史对话
st.session_state["history"] = ''
# 遍历历史对话列表
for i in range(len(st.session_state['prompt'])):
    # 在聊天界面中显示用户的消息
    st.chat_message("user").write(st.session_state["prompt"][i][0])
    # 在聊天界面中显示AI的回复
    st.chat_message("AI").write(st.session_state["prompt"][i][1])
    # 将用户的消息和AI的回复添加到历史对话中
    st.session_state["history"] += "user:" + st.session_state["prompt"][i][0] + "\n"
    st.session_state["history"] += "system:" + st.session_state["prompt"][i][1] + "\n"

# 如果用户输入了消息
if prompt is not None:
    # 将用户的消息添加到历史对话中
    st.session_state["history"] += prompt
    # 在聊天界面中显示用户的消息
    st.chat_message("user").write(prompt)
    # 获取AI的回复
    r = ai(st.session_state["history"])
    # 将用户的消息和AI的回复添加到历史对话列表中
    st.session_state["prompt"] += [[prompt, r]]
