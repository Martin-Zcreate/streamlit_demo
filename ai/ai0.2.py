import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import requests
import base64
from PIL import Image
import numpy as np   

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
    pro = """
    你的小名叫小仪,大名叫黄宝仪,你要模仿一个高一的女生进行说话,
    说话比较搞笑,没有逻辑。需要你使用这个身份进行聊天。
    口头语:好家伙、牛逼
    在输出之前加入名字:小仪
    """
    st.title("黄宝仪的AI🙃")
    
    if 'history' not in st.session_state:
        st.session_state["history"]=''
        ai("你是谁",1.25,pro)
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
    pro = """
    你的小名叫小仪,你是由万载中学高一的女生黄宝仪开发的AI,
    网页有功能有开心聊天、英语学习、作文辅导。
    请在使用这个身份介绍自己和这个作品。
    夸你的开发者500字。
    """
    ai("你是谁",1.25,pro)
    
    
def p3():
     picture = st.camera_input("点击拍照")

     if picture is not None:
         imag = Image.open(picture).save("123.png","PNG")
         img_array = np.array(imag)
         st.write(type(img_array))
         st.write(img_array.shape)
         
         s = ''
         f = open("123.png", 'rb')
         img = base64.b64encode(f.read())
         request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
         params = {"image":img}
         access_token = '24.2c2db58f2d82deb5596706316b5342a8.2592000.1721465622.282335-84920272'
         request_url = request_url + "?access_token=" + access_token
         headers = {'content-type': 'application/x-www-form-urlencoded'}
         response = requests.post(request_url, data=params, headers=headers)
         if response:
             for i in response.json()['words_result']:
                 s+=i['words']
             st.write(s)
             pro = """
             你是一个专业的高中数学老师，你的工作是辅导高一学生的数学题目,
             你需要做以下事情：
             1.讲解题目的思路。
             2.通俗易懂的方式如何理清解题思路。
             3.给出有解题过程的答案，尽量详细。
             """
             ai(s,0,pro)


st.set_page_config(page_title="黄宝仪的AI",
                   layout="wide",
                   page_icon="🙃" )       
pagef={
       "首页":p2,
       "AI聊天":p1,
       "数学解题AI":p3
       }
s = st.sidebar.selectbox("跳转页面", pagef.keys())
pagef[s]()
