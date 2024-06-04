import streamlit as st
from openai import OpenAI
import pandas as pd
import os

st.set_page_config(page_title="智酷AI助手", layout="centered", page_icon="🤖")  
st.title("智酷AI助手")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "chat_history" not in st.session_state:  
    st.session_state["chat_history"] = [] 
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False
if 'pro' not in st.session_state:
    st.session_state['pro'] = ''
if 'df' not in st.session_state:
    st.session_state['df'] = []
if 'file_path' not in st.session_state:
    st.session_state['file_path'] = '聊天记录/聊天记录.csv'

def output_data():
    st.session_state['pro'] = ''
    t = len(st.session_state['df'])-10
    if t<0:
        t=0
    for i in range(t,len(st.session_state['df'])):
        user_info=st.chat_message("user")
        user_content=st.session_state['df'].loc[i,'user']
        user_info.write(user_content)
        
        assistant_info=st.chat_message("assistant")
        assistant_content=st.session_state['df'].loc[i,'assistant']
        assistant_info.write(assistant_content)

        st.session_state['pro'] += "user:"+user_content+"\n"
        st.session_state['pro'] += "system:"+assistant_content+"\n"

if st.session_state['initialized'] == False:
    if os.path.exists(st.session_state['file_path']):
        st.session_state['df'] = pd.read_csv(st.session_state['file_path'])
    else:
        st.session_state['df'].to_csv(st.session_state['file_path'], index=False)
    output_data()
    st.session_state['initialized'] = True

def main(prompt):
    s = ""
    client = OpenAI(api_key="sk-fb2b9c1cc9934d1890b659d7a147f18d", base_url="https://api.deepseek.com/")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是智酷机器人开发的AI助手,你可以写作文,做数学题目,学习英语"},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    
    user_info=st.chat_message("user")
    user_info.write(user_input)
    
    assistant_info=st.chat_message("assistant")
    empty_p = assistant_info.empty()
    for i in response:
        s+=i.choices[0].delta.content
        empty_p.write(s)
    return s

if __name__ == '__main__':
    user_input=st.chat_input("我们来对话吧")
        
    if user_input is not None:
        progrss_bar=st.empty()
        with st.spinner("内容已提交,正在解答,请等待!"):
            output_data()
            st.session_state['pro'] += user_input
            feedback = main(st.session_state['pro'])
        if feedback:
            progrss_bar.progress(100)
            st.session_state['chat_history']=[[user_input,feedback]]
            new_df = pd.DataFrame(st.session_state["chat_history"], columns=['user', 'assistant'])
            st.session_state['df'] = pd.concat([st.session_state['df'], new_df], ignore_index=True)
            # 保存更新后的数据到csv文件
            st.session_state['df'].to_csv(st.session_state['file_path'], index=False)
        else:
            st.info("🤔对不起,我无法回答这个问题!请换一个问题.")

            
            
            
            
            
            
            
            
            
            
            
