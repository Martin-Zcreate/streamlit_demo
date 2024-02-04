# 导入必要的库，用于构建网页和处理数据
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# 设置页面配置，包括标题、布局和图标
st.set_page_config(page_title="杨岱铭的智能英语教练", layout="centered", page_icon="👦")

# 设置API密钥和密钥，用于访问百度AI平台
API_KEY = "dzAbTdjG6Tv7dg2R6V1fLgXL"
SECRET_KEY = "24GdUqOz4FlhQpGGGPntxBmKN8obgktq"


# 定义函数p1，用于显示欢迎信息
def p1():
   st.markdown("# 欢迎来到我的主页")



# 定义内部函数get_access_token，用于获取access_token
def get_access_token():
    # 构建请求URL
    url = "https://aip.baidubce.com/oauth/2.0/token"
    # 设置请求参数
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    # 发送POST请求并获取access_token
    return str(requests.post(url, params=params).json().get("access_token"))

# 定义内部函数main，用于调用百度AI平台的接口
def main1(prompt):
    # 构建请求URL，包括获取的access_token
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()

    # 构建请求数据，包含用户输入
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    # 设置请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送POST请求并获取响应
    response = requests.request("POST", url, headers=headers, data=payload)

    # 返回响应文本
    return response.text



# 定义函数p2，包含主逻辑
def p2():
    if "chat_history" not in st.session_state:  
        st.session_state["chat_history"] = []

    st.title("👦杨岱铭的智能英语教练")
    st.markdown("""
                这是我做的超级酷的智能英语教练，它就像一个会说话的电脑朋友。\n
                你只需要告诉它你想知道的英语问题，比如“我喜欢苹果英语怎么说？”\n
                它就会回答你“I like apples”。这个教练还能给我讲英语故事，帮我学新单词。\n
                它就像一个会动的英语书，而且还能和我聊天呢！\n
                如果你想试试，就来找我的智能英语教练吧，它真的很有趣哦！\n
                
                """)
    # 获取用户输入
    user_input = st.chat_input("请输入答案")

    # 在侧边栏添加按钮和功能
    with st.sidebar:
        # 清空对话历史的按钮
        if st.sidebar.button("🙅清空对话历史"):
            st.session_state["chat_history"] = []
        # 开始学习的按钮
        if st.sidebar.button("🧐开始学习英语吧"):
            user_input = """
                我叫杨岱铭,你叫李老师,请你以后这样称呼我和你,
                我是一个6年级的初中生.
                你是一个专业的6年级英语老师,请使用中文进行交流.
                我想让你教我读英语文章,背英语单词,
                请你提供一篇6年级人教版教材内的文章(字数少于100个单词),
                并提取其中5个重点词汇,在词汇后面写出单词含义,例如(like-喜欢)
            """
     
        if st.sidebar.button("😻学习重点词汇"):
            user_input = """
                请你随机抽取小学6年级的英语单词5个,你输出英文(不要中文解释),我说中文,你判断对错
            """
        
         
         

    # 如果用户输入不为空
    if user_input is not None:
        # 创建进度条
        progress_bar = st.empty()
        # 使用spinner显示加载状态
        with st.spinner("内容已提交,文心一言4.0模型正在回答中!"):
            # 调用main函数获取AI的回答
            feedback = json.loads(main1(user_input))["result"]
            # 如果有回答
            if feedback:
                # 更新进度条
                progress_bar.progress(100)  # 等待100ms清空
                # 将用户输入和AI回答添加到会话状态
                st.session_state['chat_history'].append((user_input, feedback))
                # 遍历会话历史并显示
                for i in range(len(st.session_state["chat_history"])):
                    # 显示用户信息
                    user_info = st.chat_message("user")
                    user_content = st.session_state['chat_history'][i][0]
                    user_info.write(user_content)

                    # 显示AI助手信息
                    assistant_info = st.chat_message("assistant")
                    assistant_content = st.session_state['chat_history'][i][1]
                    assistant_info.write(assistant_content)

            # 如果没有回答
            else:
                # 显示错误信息
                st.info("对不起,回答不了这个问题,请换一个问题")

# 在侧边栏显示页面选择
with st.sidebar:
    st.markdown("# 👦杨岱铭的个人网页")
   # 定义页面内容
pagef = {
    "杨岱铭的主页": p2,
    "副主页": p1
}

# 让用户选择页面
s = st.sidebar.selectbox("选择页面", pagef.keys())
# 根据选择调用对应的页面函数
pagef[s]()
