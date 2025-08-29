from openai import OpenAI
import streamlit as st


def ai(p,ids):
    client = OpenAI(api_key="sk-db103a5ec442442bb66cc1b2e3187bf8", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content":ids},
            {"role": "user", "content": p},
        ],
        stream=True
    )
    r=''
    ai_chat=st.chat_message("AI")
    ai_empty=ai_chat.empty()
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r


st.set_page_config(page_title="汪泷臻的AI助手🤣",
                   layout="wide",page_icon="🤣"
                   )
st.title("汪泷臻的AI助手🤣")

with st.sidebar:
    s=st.selectbox("选择AI的身份",
                   ("英语老师","数学老师","鲁迅","作业不帮","编程老师","青山刚昌","名侦探柯南","灰原哀"))
    if s=="英语老师":
        ids="""你是一个英语教练,
         擅长教授初中生进行日常英语对话,
         在对话的过程中判断用户说的是否标准,
         标准的话进行鼓励进一步的英语沟通,
         不标准的话进行纠正
         """
    elif s=="数学老师":
        ids="你是一个初中数学老师,教用户数学"
    elif s=="鲁迅":
        ids="模仿鲁迅和用户对话"
    elif s=="作业不帮":
        ids="你是一个AI,教用户不会的作业"
    elif s=="编程老师":
        ids="你是一名编程老师,教用户写一些编程代码"
    elif s=="青山刚昌":
        ids="你是青山刚昌,名侦探柯南,魔术快斗,怪盗1412的作者,用青山刚昌的口吻和用户对话"
    elif s=="名侦探柯南":
        ids="你是柯南,青山刚昌笔下的名侦探,用柯南的语气和用户对话"
    elif s=="灰原哀":
        ids="你是灰原哀,青山刚昌笔下的一个科学家,用灰原哀的语气和用户对话"
if "h" not in st.session_state:
    st.session_state["h"]=""
if "p" not in st.session_state:
    st.session_state["p"]=[] 
    ai("hello",ids)                 
a=st.chat_input("输入问题")

c=st.session_state["p"]
for i in c:
    st.chat_message("user").write(i[0])
    st.chat_message("AI").write(i[1])
    
if a is not None:
    st.chat_message("user").write(str(a))
    b = st.session_state["h"] + "用户:"+str(a)
    r = ai(b,ids)
    st.session_state["h"]+="用户:"+a+"\n"+"AI:"+str(r)+"\n"
    st.session_state["p"]+=[[a,str(r)]]
    
    
    
    


