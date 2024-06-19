import streamlit as st
import pandas as pd
from openai import OpenAI
import os



def output():
    for i in  range(len(st.session_state['df'])):
        st.chat_message("user").write(st.session_state['df'].loc[i,"用户"])
        st.chat_message("AI").write(st.session_state['df'].loc[i,"AI"])
        st.session_state["history"]+="user:"+st.session_state['df'].loc[i,"用户"]+"\n"
        st.session_state["history"]+="system:"+st.session_state['df'].loc[i,"AI"]+"\n"
    
    

def ai(prompt,temperature,pro):
    r=''


    client = OpenAI(api_key="sk-d7f5a176ad7546429ca5c9681c81b899", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": pro},
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

def p1():
    
    pro="""你的小名叫小仪,大名叫黄宝仪,
    你要模仿一个高一女生进行说话,
    说话有点跳脱,社交恐怖分子.
    ,需要你使用这个身份进行聊天
    在输出之前加入名字:小仪
    """
    st.title("小仪")
    
    
    if 'history' not in st.session_state:
        st.session_state["history"]=''
        ai("你是谁",1,pro)
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
        st.session_state["create"]== True
            
            
    
    
    
    st.session_state["history"]=''    
    output()
    prompt=st.chat_input("请输入")
    if prompt is not None:
        st.session_state["history"]+=prompt
        
            
            
            
        st.chat_message("user").write(prompt)
        
        
        
        
        r=ai(st.session_state["history"],1.25,pro)
        st.session_state["prompt"]=[[prompt,r]]
        new_df=pd.DataFrame(st.session_state["prompt"],columns=["用户","AI"])
        st.session_state["df"]=pd.concat([st.session_state["df"],new_df],ignore_index=True)
        st.session_state["df"].to_csv(st.session_state["file"],index=False)
        
def p2():
    st.title("首页")
    pro="""
    你的小名叫小仪,你是由一个高一女生开发的ai,请使用这个身份介绍你自己,夸你的开发者500字
    """
    ai("你是谁",1.25,pro)
        
        
        
        
st.set_page_config(page_title="小仪",
                   layout="wide",
                   page_icon="🐵")

pagef={
       "首页":p2,
       "ai聊天":p1,
       
       
       
       }    
s=st.sidebar.selectbox("",pagef.keys() )    
pagef[s]()   

