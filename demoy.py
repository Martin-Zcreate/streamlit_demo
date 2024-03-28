import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

st.set_page_config(page_title="英语学习机", layout="centered", page_icon="🤖")  
  
API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 

def p1():
    
    st.title('智能英语学习机')#应用名称
    st.write("欢迎来到英语学习专区 👋作者:中国  杨岱铭   你好吗(｡･∀･)ﾉﾞ嗨")
    #video_file = open("https://pixabay.com/en/videos/star-long-exposure-starry-sky-sky-6962/", 'rb')
    #video_bytes = video_file.read()
    #st.video("https://www.bilibili.com/video/BV1Gc411v7g1/?spm_id_from=333.1073.high_energy.content.click")
    



 

    st.markdown("""
                专为英语而生\n
                版本1.0\n
                它可以:\n
                    1.翻译(单词,词组和文章)
                    2.生成一篇英语文章(3-6年级)
                    3.我写英文你写中文
                    4.我写中文你写英文
                    5.英语知识点(3-6年级)
                制作不易,不喜勿喷🤗🤗🤗
                
                """
    )
    
    #st.image('AAA.png', caption='windows11出品,必是精品')



def p2():
    if "chat_history" not in st.session_state:  
        st.session_state["chat_history"] = []  
      
    def main(prompt):  
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()  
      
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

    if __name__== '__main__':
        st.title("😲杨岱铭🐔英语学习教练💕💕💕杨岱铭出品,必是精品☺️☺️☺️☺️")
        st.markdown("制作不易,不喜勿喷🤗🤗🤗")
        user_input = st.chat_input("请输入答案")
        with st.sidebar:
            if st.sidebar.button('清空聊天历史'):
                st.session_state['chat_history']=[]
            
            if st.sidebar.button('新年祝福🤖'):
                    user_input="""
                        请写一个新年祝福,
                        Thank you!
                    """
            
            if st.sidebar.button('开始学习English吧🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你写一个6年级的文章(50个单词以内)并提取重点单词,
                        Thank you!
                    """
            
            if st.sidebar.button('开始翻译英文吧🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你写一个6年级的英语单词(不包括中文),
                        我翻译,你判断。
                        Thank you!
                    """
            
            if st.sidebar.button('开始翻译中文吧🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你写一个6年级的英语单词的中文(不包括英文),
                        我翻译,你判断。
                        Thank you!
                    """
            
            if st.sidebar.button('AI翻译(英译中)🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你帮我翻译,
                        Thank you!
                    """
            
            if st.sidebar.button('AI翻译(中译英)🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你帮我翻译,
                        Thank you!
                    """
            
            if st.sidebar.button('AI知识点🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你帮我写一个知识点,6年级的(不含题目,短一点),
                        Thank you!
                    """
            
            if st.sidebar.button('AI出题🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你帮我出一个6年级的英语题(不含答案,不要太难),
                        我写答案，你判断,
                        Thank you!
                    """
            
            if st.sidebar.button('English的来历🦾'):
                    user_input="""
                        我是杨岱铭,请你以后这样称呼我。
                        你是一个专业的6年级英语老师,
                        你叫纸张，
                        我想让你教我English文章,背单词,
                        请你说出English的来历,
                        Thank you!
                    """
           
            if st.sidebar.button('自我介绍🤖'):
                    user_input="""
                        你是一个专业的6年级英语老师,
                        你是百度老师,
                        请自我介绍,
                        用英文,
                        你来自万载,
                        Thank you!
                    """
            st.markdown("制作不易,不喜勿喷🤗🤗🤗")
    
    

    
    if user_input is not None:
        progress_bar = st.empty()
        
        with st.spinner("已提交,文心一言4.0正在回答ing......"):
            feedback = json.loads(main(user_input))['result']
            if feedback:
                progress_bar.progress(100)
                st.session_state['chat_history'].append((user_input,feedback))
                for i in range(len(st.session_state['chat_history'])):
                    user_info=st.chat_message('user')
                    user_content=st.session_state['chat_history'][i][0]
                    user_info.write(user_content)
                    
                    assistant_info=st.chat_message('assistant')
                    assistant_content=st.session_state['chat_history'][i][1]
                    assistant_info.write(assistant_content)
                    
                    
            else:
                st.info('不能回答,斯密达😂')

def p3():
    st.title("智能英语学习机")
    st.markdown("""
                该网页为了孩子的英语而生,\n
                可以让老师更方便地备课,\n
                让学生跟方便地学习英语。
                如果有宝贵建议请发微软邮箱,就是Outlook.com(qqq123456131949)并留下您的大名,谢谢\n
                在此网站内,请注意您的语言文明,谢谢。\n
                制作不易,不喜勿喷🤗🤗🤗
                """)
    #st.image('UUU.png', caption='杨岱铭出品,必是精品')

def p4():
    st.title("智能英语学习机教程")
    st.markdown("""
                1.点击"选择页面"下面的框。\n
                2.选择选项:\n
                    ①杨岱铭的主页:\n
                        ①了解网页信息,版本,开发者等。
                    ②网页简介:\n
                        ①可以了解这个网页。\n
                3. 在问答区问答时,请注意您的语言文明,Tankyou!
                制作不易,不喜勿喷🤗🤗🤗
                """)
    
        
    
pagef = {
    "学习专区(语文、数学、英语都可以,按钮以英语为主)" : p2,
    "杨岱铭的主页" : p1,
    "网页简介" : p3,
    "教程" : p4
    }
    
s = st.sidebar.selectbox("选择页面",pagef.keys())
pagef[s]()



