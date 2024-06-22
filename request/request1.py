import requests
import time
import random
import streamlit as st
import pandas as pd
import os
import datetime

file = "123.csv"

if not os.path.exists(file):
    df = pd.DataFrame(columns=["消息","时间"])
    df.to_csv(file)

# 你的Streamlit应用程序的URL
app_url = ["https://liushaofeng.streamlit.app",
           "https://ai02py.streamlit.app/",
           "https://gaopeixing.streamlit.app/",
           "https://liuyanapp.streamlit.app/",
           "https://liuyanchen.streamlit.app/",
           "https://wuzhehan1.streamlit.app/",
           "https://xinjianxi.streamlit.app/",
           "https://yuanzixuan.streamlit.app/",
           "https://yushengyuan.streamlit.app/",
           "https://zhaiyixuan1.streamlit.app/",
           "https://zhaoyijie.streamlit.app/",
           "https://zhikurobot.streamlit.app/",
           "https://zkrobot.streamlit.app/",
           "https://chenwenke.streamlit.app/",
           "https://daizhenming.streamlit.app/",
           "https://wangxy.streamlit.app/",
           "https://yangdaiming.streamlit.app/",
           "https://huangbaoyi.streamlit.app/",
           "https://wahutao.streamlit.app/",
           "https://lanruicheng.streamlit.app/",
           "https://liushaofeng.streamlit.app/",
           "https://musicapppy-cxvciftn6wnediwqdeyuth.streamlit.app/",
           "https://qixing.streamlit.app/",
           "https://wangheyu.streamlit.app/",
           "https://wordspy-mpmtjhadzeyf5qchc97eex.streamlit.app/",
           "https://wuzehan.streamlit.app/",
           "https://zhaiyixuan.streamlit.app/",
           "https://request2.streamlit.app/"
           ]

def keep_alive():
    df = pd.read_csv(file)
    for i in range(len(df)):
        a2 = str(df.loc[i,"消息"])
        a3 = str(df.loc[i,"时间"])
        st.chat_message("user").write(f"{a2}:------{a3}")
    
    
    # 发送GET请求到你的应用程序
    s1 = s2 = 0
    for i in app_url:
        response = requests.get(i)
        if response.status_code == 200:
            st.write(f"成功:{i}")
            s1+=1
        else:
            st.write(f"失败:{i}")
            s2+=1
        time.sleep(random.randint(0,5))
    st.write(f"成功:{s1},失败:{s2}")
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    p=[[f"成功:{s1},失败:{s2}",t]]
    newdf = pd.DataFrame(p,columns=["消息","时间"])
    df = pd.concat([df,newdf],ignore_index=False)
    df.to_csv(file)

# 设置定期访问的时间间隔（以秒为单位）
interval = 3600*12  # 每12H访问一次

while True:
    keep_alive()
    time.sleep(interval)
