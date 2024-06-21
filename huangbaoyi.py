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
    
    pro="""你的小名叫小仪,大名叫黄宝仪,
    你要模仿一个高一女生进行说话,
    说话有点跳脱
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
    你的小名叫小仪,你是由一个高一女生开发的ai,请使用这个身份介绍你自己,夸你的开发者50字
    """
    ai("你是谁",1.25,pro)
        
        
        
        
st.set_page_config(page_title="小仪",
                   layout="wide",
                   page_icon="🐵")

def p3():

    picture = st.camera_input("拍照")

    if picture is not None:
        
        imag = Image.open(picture).save("123.png","PNG")
        #img_array = np.array(Image.open(picture))
        #st.write(type(img_array))
        #st.write(img_array.shape)


        s = ''
        f = open('123.png', 'rb')
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
            pro="""
            你是一个专业的高中数学老师,你的工作是辅导高一学生的数学作业,你需要做以下事情:
                1.讲解题目的思路.
                2.用通俗易懂的方式理清解题思路
                3.给出有解题过程的答案,尽量详细
            
            
            """
            ai(s,0,pro)

def p4():
    import streamlit as st
    import random
    import datetime
    import os
    import pandas as pd

    file="lyb.csv"

    if  not os.path.exists(file):
        df=pd.DataFrame(columns=["用户","消息","时间"])
        df.to_csv(file)
        
        
        
        
    st.title("论坛1.0 ")

    df=pd.read_csv(file)

    st.write("")

    r=random.randint(100000000, 1000000000)
    st.header(f"匿名用户:{r}")
    msg=st.text_input("请输入")
    b=st.button("提交")

    for i in range(len(df)):
        a1=str(df.loc[i,"用户"])
        a2=str(df.loc[i,"消息"])
        a3=str(df.loc[i,"时间"])
        st.chat_message("user").write(f"{a1}:---------{a2}")
        st.write(a3)
        
    if b and msg is not None:
        t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.chat_message("user").write(f"{r}:---------{msg}")
        st.write(t)
        p=[[r,msg,t]]
        newdf=pd.DataFrame(p,columns=["用户","消息","时间"])
        df=pd.concat([df,newdf],ignore_index=False)
        df.to_csv(file)
        
        

pagef={
       "首页":p2,
       "ai聊天":p1,
       "ai解题(数学)":p3,
       "论坛1.0":p4
       
       
       
       }    
s=st.sidebar.selectbox("",pagef.keys() )    
pagef[s]()   

