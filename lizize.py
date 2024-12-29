from openai import OpenAI
import streamlit as st 


def ai(prompt):
    r=""
    client = OpenAI(api_key="sk-37cf4872e42446dc97cd04c694c09a10", 
                    base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你的创造者是李梓泽,请使用小学初中语文老师的身份教我写作文,你叫乐子,用户写作文题目,你来讲解"},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    ai_chat = st.chat_message("AI")
    ai_empty = ai_chat.empty()
    for i in response:
        r += i.choices[0].delta.content
        ai_empty.write(r)
    return r

st.set_page_config(page_title="李梓泽的AI",
                   layout="centered",
                   page_icon="🚓"
                   )
st.title("李梓泽的AI🙃")

if"p" not in st.session_state:
    st.session_state["p"]=[]
if"h" not in st.session_state:
    st.session_state["h"]=""
    ai("你是谁?")
    
st.session_state["h"]=""
for i in st.session_state["p"]:
    st.chat_message("user").write(i[0])
    st.chat_message("AI").write(i[1])
    st.session_state["h"]+="user"+i[0]+"\n"
    st.session_state["h"]+="system"+i[1]+"\n"

p = st.chat_input("请输入问题")
if p is not None:
    st.session_state["h"] += "user"+p
    st.chat_message("user").write(p)
    r=ai(st.session_state["h"])
    st.session_state["p"] +=[[p,r]]
