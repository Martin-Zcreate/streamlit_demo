import streamlit as st
import pandas as pd
import numpy as np                                   
import requests 
import json  
 
st.set_page_config(page_title="智能简单方程学习机", layout="centered", page_icon="👋")  
API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 

def p1():
    st.title("智能简单方程学习机")
    st.write("👋欢迎来到我的作品👋ヾ(≧ ▽ ≦)ゝ")
    st.markdown(
        """
        此程序能帮助你:\n
        1.丰富数学方程知识.\n
        2.教你解方程方法.\n
        3.帮你出易错方程题.\n
        4.帮你批改你做的方程是否正确.\n
        作者:陈文柯.
        """
        )
    st.sidebar.success("选择一个选项")
    
    
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
        st.title("q(≧▽≦q)请问我,陈文柯老师随时回答哦!")
        user_input=st.chat_input("请输入题目")
        
        with st.sidebar:
            if st.sidebar.button("清空内容"):
                st.session_state['chat_history'] = []
            
            if st.sidebar.button("教我解简单方程吧(●'◡'●)!"):
                user_input="""
                我叫陈文柯,请你以后这样称呼我!
                我是一个智商较高的5年级小学生,
                你是一个专业的5年级数学老师,
                请你告诉我如何解一元一次方程和二元一次方程,
                如5x=10,2x-2=0,10-x=6,x-14=5.
                二元一次方程:3x+2y=10,2x+2y=9,,二元一次方程:5x+5-y=7,2x+y+7=10. 
                """
                
            if st.sidebar.button("出一元一次方程."):
                user_input="""
                我是一个5年级小学生,
                请提供三道较难一点的一元一次方程.
                请你不要写出答案和思路,
                我来回答这个问题,请你判断是否正确🙂.
                """
                
            if st.sidebar.button("出二元一次方程."):
                user_input="""
                我是一个5年级小学生,
                请提供我一道二元一次方程.
                请你不要写出答案和思路,
                我来回答这个问题,请你判断是否正确🙂.
                """  
                
            wt = st.sidebar.chat_input("请输入方程和答案")
            if wt:
                user_input = wt + "请判断这个方程的答案是否正确,不正确的话请教我一下"
            
        with st.sidebar:
            st.markdown("# 陈文柯的网页")
            
        if user_input is not None:
            progrss_bar=st.empty()
            with st.spinner("内容已提交,正在解答,请等待!"):
                feedback = json.loads(main(user_input))["result"]
            if feedback:
                progrss_bar.progress(100)
                st.session_state['chat_history'].append((user_input,feedback))
                for i in range(len(st.session_state["chat_history"])):
                    user_info=st.chat_message("user")
                    user_content=st.session_state['chat_history'][i][0]
                    user_info.write(user_content)
                    
                    assistant_info=st.chat_message("assistant")
                    assistant_content=st.session_state['chat_history'][i][1]
                    assistant_info.write(assistant_content)
            else:
                st.info("🤔对不起,我无法回答这个问题!请换一个问题.")
            
pagef={
       "陈文柯的主页":p1,
       "陈文柯的帮助":p2
       }
s=st.sidebar.selectbox("选择页面",pagef.keys())
pagef[s]()