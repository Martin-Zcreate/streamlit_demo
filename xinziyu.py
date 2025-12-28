import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="辛子瑜",
                   layout="wide",
                   page_icon="♥")
    
st.title("辛子瑜AI助手🎃")



def ai(x):
    r=""
    client = OpenAI(
        api_key="sk-db103a5ec442442bb66cc1b2e3187bf8",
        base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """
             
             你是辛子瑜的作文帮手,专门教六年级的语文作文,
             用户会给你一个作文题目和作文类型,
             你需要写一篇六年级学生水平的作文.
             字数要求600字.
             男孩子
             用户身份背景,万载一小,六年级三班.
             家住在万载,11岁,爸爸妈妈在家里一起生活
             """},
            {"role": "user", "content": x},
        ],
        stream=True
    )
    ai_chat = st.chat_message("AI")
    ai_empty = ai_chat.empty()         
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
        
    return r
    
if "pro" not in st.session_state:
    st.session_state["por"] = []
if "h" not in st.session_state:
    st.session_state["h"] = ""
    ai("骂辛子瑜,用的手法200字")

p = st.chat_input("输入对话")

st.session_state["h"]=""

for i in range(len(st.session_state["pro"])):
    st.chat_message("user").write(st.session_state["pro"][i][0])
    st.chat_message("AI").write(st.session_state["pro"][i][1])
    st.session_state["h"]+="user:"+st.session_state["pro"][i][0]
    st.session_state["h"]+="AI:"+st.session_state["pro"][i][1]
    
    
    
if p is not None:
    st.session_state["h"]+=p
    st.chat_message("user").write(p)
    s = ai(st.session_state["h"])
    st.session_state["pro"]+=[[p,s]]
