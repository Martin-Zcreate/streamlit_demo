from openai import OpenAI
import streamlit as st

def ai(prompt):
    r = ''
    client = OpenAI(api_key="sk-d7f5a176ad7546429ca5c9681c81b899", base_url="https://api.deepseek.com/")
        
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你的名字叫总统,你的开发者是刘彦辰,请你使用这个身份介绍自己"},
            {"role": "user", "content": prompt},
        ],
        stream=True 
    )
    ai_chat = st.chat_message("AI") 
    ai_empty = ai_chat.empty()
    for i in response:
        
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r
 
st.set_page_config(page_title="智酷刘彦辰助手",
                               layout="wide",
                               page_icon="👀👀"
                               )
st.title("智酷刘彦辰助手💂🏿‍♀️")

if "prompt" not in st.session_state:
    st.session_state["prompt"]=[]
if "history" not in st.session_state:
    st.session_state["history"]=""
    ai("你是谁")
    
prompt = st.chat_input("请输入")
st.session_state["history"]=""

for i in range(len(st.session_state["prompt"])):
    st_chat = st.chat_message("user").write(st.session_state["prompt"][i][0]) 
    st_chat = st.chat_message("AI").write(st.session_state["prompt"][i][1]) 
    st.session_state["history"]+="user:"+st.session_state["prompt"][i][0]+"\n"
    st.session_state["history"]+="system:"+st.session_state["prompt"][i][1]+"\n"
    


if prompt is not None:
    st.session_state["history"]+=prompt
    st_chat = st.chat_message("user").write(prompt)
    
    
    r=ai(st.session_state["history"])
    st.session_state["prompt"]+=[[prompt,r]]
    
    
