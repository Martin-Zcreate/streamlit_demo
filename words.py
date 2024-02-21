import streamlit as st
import pandas as pd
from io import StringIO
import jieba
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
import requests  
import json

if "chat_history" not in st.session_state:  
    st.session_state["chat_history"] = [] 

API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 

def get_access_token():  
        """  
        使用 AK，SK 生成鉴权签名（Access Token）  
        :return: access_token，或是None(如果错误)  
        """  
        url = "https://aip.baidubce.com/oauth/2.0/token"  
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}  
        return str(requests.post(url, params=params).json().get("access_token"))


def ai(prompt):  
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



def p1():
    st.title("智酷机器人的主页")
    
    a = ["语文","数学","英语"]
    b = [0,0,0]
    b[0] = st.number_input("输入语文成绩",step=1)
    b[1] = st.number_input("输入数学成绩",step=1)
    b[2] = st.number_input("输入英语成绩",step=1)
    d = dict(zip(a, b))
    
    if st.button("开始画图"):
        c = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(a, b)],
                radius=["30%", "75%"],
                center=["50%", "50%"],
                rosetype="area",
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="成绩分布图"))
        )
        st_pyecharts(c)
        
        score = f"""
        我是一个大一交通系的学生,以下是我的考试成绩,满分为100分,
        请为我分析一下这个成绩,并且给出弱势成绩的提升方案,需要详细具体的步骤.{d}
        """
        
        with st.spinner("文心一言4.0正在分析中,请耐心等待...."):
            feedback = json.loads(ai(score))["result"]
            if feedback:
                ai_info = st.chat_message("ai")
                ai_info.write(feedback)
        

def p2():
    uploaded_file = st.file_uploader("Choose a file")
    
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)
        st.write(type(stringio))
    
    txt = st.text_area(
            "",
            ""
            "",
            )

    st.write(f'你输入了{len(txt)}个字.')

    if st.button("开始分析和写读后感"):
        
        list1 = jieba.lcut(txt)
        counts = {}
        # list2 = []
        for i in list1:
            if len(i) == 1:
                continue
            # list2+=[i]
            counts[i] = counts.get(i,0)+1
            
        list3 = list(counts.items())
        list3.sort(key=lambda x: x[1],reverse=1)
    
        list6 = list3[0:100]
        dict1 = dict(list6)
        list4 = list(dict1.keys())
        list5 = list(dict1.values())
    
    
        c = (
            Bar()
            .add_xaxis(list4)
            .add_yaxis("", list5, color=Faker.rand_color())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="三国演义词频统计"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            )
        )
        st_pyecharts(c)
        
        ai_words = f"""
        我是一个6年级的小学生,我需要在寒假写一篇文章的读后感,
        字数要求500字以上.一下就是这篇文章.{txt}
        
        """
        with st.spinner("文心一言4.0正在分析中,请耐心等待...."):
            feedback = json.loads(ai(ai_words))["result"]
            if feedback:
                ai_info = st.chat_message("ai")
                ai_info.write(feedback)
    
    
def p3():
    st.title("AI聊天🐱")
    user_input =st.chat_input("在这里输入")
    
    with st.sidebar:
        s1 = st.sidebar.selectbox("写哪种类型的检讨书",
                                  ("卫生","作业","玩手机"))
        
        if st.sidebar.button("开始写"):
            user_input = f"""
            我是一个交通管理系的大一的学生,我的名字叫张三,
            请写一篇长度为200字的{s1}检讨书,内容格式要求完整,
            态度认真恳切,情真意切,富有感情.
            """
        
    
    if user_input:
        progress_bar = st.empty()
        with st.spinner("内容已提交,文心一言4.0正在回答中"):
            feedback = json.loads(ai(user_input))["result"]
            if feedback:
                progress_bar.progress(100)
                st.session_state["chat_history"].append((user_input,feedback))
                
                for i in range(len(st.session_state["chat_history"])):
                    user_info = st.chat_message("human")
                    user_content = st.session_state["chat_history"][i][0]
                    user_info.write(user_content)
                    
                    assistant_info = st.chat_message("ai")
                    assistant_content = st.session_state["chat_history"][i][1]
                    assistant_info.write(assistant_content)
            else:
                st.info("无法回答,请重新输入!")

def p4():
    st.title("开心一下😃")
    st.title("NO 1.年龄选择器😃")
    if st.checkbox("选择年龄👱"):
        age = st.slider('你的年龄是多少?', 0, 130, 25)
        st.write(f"你的年龄是{age}")
    
    st.title("NO 2.喜欢的电影😃")
    if st.checkbox("选择电影🎮"):
        movie = st.multiselect("选择你喜欢的电影", ["流浪地球","复仇者联盟"],["流浪地球"])
        st.write(f"你的电影是{movie}")
        
    st.title("NO 3.来这里听音乐😃")
    if st.checkbox("选择音乐🎵"):
        music = st.selectbox("选择你喜欢的音乐播放", ["夜曲","夜曲","夜空中最亮的星","天空之城"])
        
        audio_file = open(f'music1/{music}.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)
    
pagef = {
    "成绩分析":p1,
    "词频统计":p2,
    "AI聊天":p3,
    "娱乐":p4
    }

s = st.sidebar.selectbox("跳转网页", pagef.keys())
pagef[s]()



