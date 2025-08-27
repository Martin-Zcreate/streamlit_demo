from openai import OpenAI
import streamlit as st

if "h" not in st.session_state:
    st.session_state['h'] = ""
if "p" not in st.session_state:
    st.session_state['p'] = []
    
def ai(p):
    client = OpenAI(api_key="sk-db103a5ec442442bb66cc1b2e3187bf8", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个AI助手"},
            {"role": "user", "content": p},
        ],
        stream=True
    )
    r = ''
    ai_chat = st.chat_message("AI")
    ai_empty = ai_chat.empty()
    for i in response:
        r +=i.choices[0].delta.content
        ai_empty.write(r)
    return r



st.set_page_config(page_title="辛炎承AI助手☯",layout="wide",page_icon="☯")
st.title("辛炎承AI助手☯")
ai("给用户写一首欢迎小诗,网页的制作者是辛炎承")


a = st.chat_input("请输入问题")

c = st.session_state['p']
for i in c:
    st.chat_message("user").write(i[0])
    st.chat_message("AI").write(i[1])
    
if a is not None:
    st.chat_message("user").write(str(a))
    b = st.session_state['h'] + "用户:"+str(a)
    r = ai(a)
    st.session_state['h'] += "用户:"+a+"\n"+"AI:"+str(r)+"\n"
    st.session_state['p']+=[[a,str(r)]]
