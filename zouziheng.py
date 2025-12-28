import streamlit as st
import os
from openai import OpenAI
st.set_page_config(page_title="周子衡のAI.一号",layout="wide",page_icon="↖%")

st.title("周子衡のAI📝")


def ai(x):
    r=""
    client = OpenAI(
        api_key="sk-db103a5ec442442bb66cc1b2e3187bf8",
        base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是周子衡的作文帮手,专门写六年级作文"},
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
    st.session_state["pro"] = []
if "h" not in st.session_state:
    st.session_state["h"] = ""
    ai("夸夸我,散文诗,80字左右,在结尾加上✨")
x=st.chat_input("说些什么吧~~~")
st.session_state["h"]=""
for i in range(len(st.session_state["pro"])):
    st.chat_message("user").write(st.session_state["pro"][i][0])
    st.chat_message("AI").write(st.session_state["pro"][i][1])
    st.session_state["h"]+="user"+st.session_state["pro"][i][0]
    st.session_state["h"]+="AI"+st.session_state["pro"][i][1]
if x is not None:
    st.session_state["h"]+=x
    st.chat_message("user").write(x)
    s=ai(st.session_state["h"])
    st.session_state["pro"]+=[[x,s]]
