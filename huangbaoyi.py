import streamlit as st
from openai import OpenAI

st.title("AI")
if 'history' not in st.session_state:
    st.session_state["history"]=''
if"prompt"not in st.session_state:
    st.session_state["prompt"]=[]
    
    


def ai(prompt,temperature):
    r=''


    client = OpenAI(api_key="sk-a018798f114c42b783fdf8c2760f49e2", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是 一个助手"},
            {"role": "user", "content": prompt},
        ],
        stream=True,
        temperature=temperature
        
    )
    ai_chat=st.chat_message("AI")
    ai_empty=ai_chat.empty()
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r
    

prompt=st.chat_input("你有什么疑问,都可以问我啊!")
if prompt is not None:
    for i in st.session_state['prompt']:
        st.chat_message("user").write(i[0])
        st.chat_message("AI").write(i[1])
        
        
        
    st.chat_message("user").write(prompt)
    
    
    st.session_state["history"]+="user:"+prompt+"\n"
    
    r=ai(st.session_state["history"],1.25)
    st.session_state["prompt"]+=[[prompt,r]]
    
    st.session_state["history"]+="system:"+r+"\n"

