import streamlit as st
import pandas as pd
from openai import OpenAI
import os

st.title("AI123")

def output():
    for i in  range(len(st.session_state['df'])):
        st.chat_message("user").write(st.session_state['df'].loc[i,"用户"])
        st.chat_message("AI").write(st.session_state['df'].loc[i,"AI"])
        st.session_state["history"]+="user:"+st.session_state['df'].loc[i,"用户"]+"\n"
        st.session_state["history"]+="system:"+st.session_state['df'].loc[i,"AI"]+"\n"
    
    
if 'history' not in st.session_state:
    st.session_state["history"]=''
if"prompt"not in st.session_state:
    st.session_state["prompt"]=[]
if "file" not in st.session_state:
    st.session_state["file"]='ai聊天记录.csv'

if "df" not in st.session_state:
    st.session_state["df"]=[]
if"create" not in st.session_state:
    st.session_state["create"]=False
if  st.session_state["create"]== False:
    if os.path.exists(st.session_state["file"]):
        st.session_state["df"]=pd.read_csv(st.session_state["file"])
    else:
        st.session_state["df"].to_csv(st.session_state["file"],index=False)
    st.session_state["create"] = True
        
        


def ai(prompt,temperature):
    r=''


    client = OpenAI(api_key="sk-d7f5a176ad7546429ca5c9681c81b899", base_url="https://api.deepseek.com")
    
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
st.session_state["history"]=''    
output()
prompt=st.chat_input("请输入")
if prompt is not None:
    
        
        
        
    st.chat_message("user").write(prompt)
    
    
    
    
    r=ai(st.session_state["history"],1.25)
    st.session_state["prompt"]=[[prompt,r]]
    new_df=pd.DataFrame(st.session_state["prompt"],columns=["用户","AI"])
    st.session_state["df"]=pd.concat([st.session_state["df"],new_df],ignore_index=True)
    st.session_state["df"].to_csv(st.session_state["file"],index=False)
    
    
    
    

