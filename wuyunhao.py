from openai import OpenAI
import streamlit as st

def ai(prompt):
    r=""
    client = OpenAI(api_key="sk-bf811718c8164f50ad0861059db1aff7", 
                    base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """
             你的创造者是万载第三中学的吴云浩,
             请使用初中老师的身份,
             你叫尤塞恩.博尔特,
          """},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    ai_chat=st.chat_message("AI")
    ai_empty=ai_chat.empty()
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r
    
st.set_page_config(page_title="吴云浩AI",
                   layout="centered",
                   page_icon="🚝"
                   )

st.title("吴云浩AI🚝")

if "p"not in st.session_state:
    st.session_state["p"]=[]
if "h"not in st.session_state:
    st.session_state["h"]=""
    ai("你是谁")

p=st.chat_input("请输入问题")
with st.sidebar:
    p1 = st.text_area("输入")
    if st.button("做数学题"):
        p=f"""你是一个专业的中学数学老师,
        你出一道{p1}数学题,用户来回答,再判断是否答对,
        然后继续出"""
    if st.button("做语文题"):
        p=f"""
        你是一个专业的中学语文老师,
        你出一个古诗填空题,用户来回答,再判断是否答对,
        然后继续出"""
    if st.button("做英语题"):
        p=f"""你是一个专业的英语老师,
        你出一个英语选择题,用户来回答,再判断是否答对,
        然后继续出"""
    if st.button("写作文"):
        p=f"""
        你是一个专业的中学作文老师,
        作文要求:{p1}
        请写出这篇作文的5个思路,详细讲解作文的写法.
        最后给出一篇范文"""


st.session_state["h"]=""
for i in st.session_state["p"]:
    st.chat_message("user").write(i[0])
    st.chat_message("AI").write(i[1])
    st.session_state["h"]+="user"+i[0]+"\n"
    st.session_state["h"]+="system"+i[1]+"\n"


if p is not None:
    st.session_state["h"]+="user"+p
    st.chat_message("user").write(p)
    r=ai( st.session_state["h"])
    st.session_state["p"]+=[[p,r]]

