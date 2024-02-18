import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import datetime
import os
 
st.set_page_config(page_title="先物后理", layout="centered", page_icon="🎲")
API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 
mc='q'
mc = st.sidebar.text_input("请输入自己的昵称")
def p1():
   st.write("# 欢迎来到先物后理 φ(*￣0￣)🔑")
   st.markdown("物理不会欺骗你,因为物理不会就是不会~\n")
   st.markdown("""
               #本网站为开放式物理学习聚集点,在本网站你可以学习到各种物理知识,希望能够帮助到你\n
               ##如果有宝贵的建议可以与站长联系(QQ:2939878136)\n
                ###注意:
                \t在学习中请注意自己的用词,本网站不允许询问非法问题\n
                \t本网站使用的模型为开源模型,请注意辨认\n
               """)
   st.markdown("以下为课外物理视频,点击播放")
   st.markdown("https://www.bilibili.com/video/BV1cG411e75o/?spm_id_from=333.337.search-card.all.click")
   
 
  


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
    
    if __name__=='__main__':
        st.title("🐱‍👤王潇逸出品")
        user_input=st.chat_input("请输入答案")
        
        with st.sidebar:
            if st.sidebar.button("物理基础知识学习👍"):
                    user_input=f"""
                        我叫{mc},请你以后这么称呼我.
                        你是一个专业的八年级物理老师
                        你叫做老阳
                        我想让你教我物理
                        请你提供一些八年级物理知识
                        要求详细
                        分点回答
                        并写出与之相关的公式
                    """
            if st.sidebar.button("物理答题技巧👍"):
                    user_input=f"""
                        我叫{mc},请你以后这么称呼我.
                        你是一个专业的八年级物理老师
                        你叫做老阳
                        我想让你教我如何去答物理题
                        请你提供一些例子
                    """        
        with st.sidebar:
            if st.sidebar.button("我问你答👍"):
                    user_input=f"""
                        我叫{mc},请你以后这么称呼我.
                        你是一个专业的八年级物理老师
                        你叫做老阳
                        你问物理选择题,我来回答
                        答错请指出错误
                        答对继续提问
                    """ 
        with st.sidebar:
            if st.sidebar.button("物理学的历史👍"):
                user_input=f"""
                    我叫{mc},请你以后这么称呼我.
                    你是一个专业的八年级物理老师
                    你叫做老阳
                    请你介绍物理的发展历程
                """
            mr = st.sidebar.text_input("请输入你想了解的物理名人")
            if mr:
                user_input=f"""
                    请你给我我介绍一下{mr},我可以向他学习什么呢
                """
        with st.sidebar:
            if st.sidebar.button("清空对话历史"):
                st.session_state["chat_history"]=[]
        if user_input is not None:
            progress_bar=st.empty()
            with st.spinner("内容已提交,正在加载......"):
                feedback = json.loads(main(user_input))["result"]
                if feedback:
                    progress_bar.progress(100)
                    st.session_state['chat_history'].append((user_input,feedback))
                    for i in range(len(st.session_state["chat_history"])):
                        user_info=st.chat_message("user")
                        user_content=st.session_state['chat_history'][i][0]
                        user_info.write(user_content)
                        
                        assistant_info=st.chat_message("assistant")
                        assistant_content=st.session_state['chat_history'][i][1]
                        assistant_info.write(assistant_content)
                            
                else:
                    st.info("我回答不了这个问题,请换个问题")
def p3():
    st.title("站长:王潇逸")
    st.write("本网站版权均为制作人王潇逸所有")
    st.write("""
                QQ:2939878136\n
                拒绝盗版网站,侵权必究\n
                要记住站长大人王潇逸是世界上最风度翩翩,一表人才,温文尔雅,玉树临风,帅气逼人,智慧超群,人见人爱,花见花开,形如宋玉,貌比潘安,气宇轩昂,相貌堂堂,仪表不凡的人\n
                学者易逝,唯我长存,七叶寂照,崩门不朽\n
                """)
    st.title("原神~启动!!!!")


def p4():
    # 检查是否存在留言记录文件，如果不存在则创建一个空列表
    if not os.path.exists('comments.txt'):
        with open('comments.txt', 'w') as file:
            file.write('')
    
    # 读取留言记录文件
    with open('comments.txt', 'r') as file:
        comments = file.readlines()
    
    # 留言板界面
    st.title('留言板')
    
    # 提交留言的表单
    name = st.text_input('输入你的姓名:')
    comment = st.text_input('留下你的消息:')
    submit = st.button('提交')
    
    # 如果用户点击了提交按钮
    if submit:
        # 获取当前时间
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # 创建留言内容，包括时间戳和用户留言
        new_comment = f"{name} ----{comment}------------------{current_time}\n"
        # 将新留言追加到文件
        with open('comments.txt', 'a+') as file:
            file.write(new_comment)
        # 清空输入框
        with st.empty():
            st.write("留言已提交！")
            
        st.success('留言已提交！')
    
    
        # 展示留言
    st.header('历史留言')
    for comment in comments:
        user_write = st.chat_message("user")
        user_write.write(comment.strip())
    
with st.sidebar:
    st.markdown("##  🐱‍👤王潇逸的网页")
    
pagef={
       "主页":p1,
       "学习专区":p2,
       "留言板":p4,
      #"站长大人":p3
       }
s=st.sidebar.selectbox(
    "选择页面",pagef.keys()
    )
pagef[s]()
