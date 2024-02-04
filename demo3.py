import streamlit as st
import pandas as pd
import numpy as np
import requests
import json


st.set_page_config(page_title="英语学习机", layout="centered", page_icon="🤖")  

API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 

def p1():
    st.markdown("# 欢迎来到我的主页")
    


def p2():
    if "chat_history" not in st.session_state:  
        st.session_state["chat_history"] = []  
      
    def main(prompt):  
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()  
      
        payload = json.dumps({  
            "messages": [  
                {  
                    "role": "user",  
                    "content": prompt  
                }  
            ]  
        })  
        headers = {  
            'Content-Type': 'application/json'  
        }  
      
        response = requests.request("POST", url, headers=headers, data=payload)  
      
        return response.text
    
    def get_access_token():  
        """  
        使用 AK，SK 生成鉴权签名（Access Token）  
        :return: access_token，或是None(如果错误)  
        """  
        url = "https://aip.baidubce.com/oauth/2.0/token"  
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}  
        return str(requests.post(url, params=params).json().get("access_token"))
    
    if __name__ == '__main__':
        st.title("👦杨岱铭的智能英语教练")
        user_input = st.chat_input("请输入答案")
        
        with st.sidebar:
            if st.sidebar.button("🧐开始学习英语吧"):
                user_input ="""
                    我叫戴震铭,请你以后这样称呼我,
                    我是一个8年级的初中生.
                    你是一个专业的8年级英语老师,
                    我想让你教我读英语文章,背英语单词,
                    请你提供一篇8年级教材内的文章(字数少于100个单词),
                    并提取其中5个重点词汇,在词汇后面写出单词含义,例如(like-喜欢)
                """
        
        
        if user_input is not None:
            progress_bar = st.empty()
            with st.spinner("内容已提交,文心一言4.0模型正在回答中!"):
                feedback = json.loads(main(user_input))["result"]
                if feedback:
                    progress_bar.progress(100)
                    st.session_state['chat_history'].append((user_input,feedback))
                    for i in range(len(st.session_state["chat_history"])):
                        user_info = st.chat_message("user")
                        user_content = st.session_state['chat_history'][i][0]
                        user_info.write(user_content)
                        
                        assistant_info = st.chat_message("assistant")
                        assistant_content = st.session_state['chat_history'][i][1]
                        assistant_info.write(assistant_content)
                        
                        with st.sidebar:
                            if st.sidebar.button("清空对话历史"):
                                st.session_state["chat_history"] = []
                else:
                    st.info("对不起,回答不了这个问题,请换一个问题")
        
        
    
with st.sidebar:
    st.markdown("# 👦杨岱铭的私人网页")
    
pagef = {
    "戴震铭的主页" : p1 ,
    "画图页面" : p2
    }

s = st.sidebar.selectbox(
    "选择页面",pagef.keys()
    )
pagef[s]()
    

