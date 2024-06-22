import requests
import time
import random
import streamlit as st
import pandas as pd
import os
import datetime

file = "re2.csv"

if not os.path.exists(file):
    df = pd.DataFrame(columns=["消息","时间"])
    df.to_csv(file)

# 你的Streamlit应用程序的URL
app_url = "https://request1.streamlit.app/"

def keep_alive():
    df = pd.read_csv(file)
    for i in range(len(df)):
        a2 = str(df.loc[i,"消息"])
        a3 = str(df.loc[i,"时间"])
        st.chat_message("user").write(f"{a2}:------{a3}")
    
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # 发送GET请求到你的应用程序
    response = requests.get(app_url)
    if response.status_code == 200:
        st.write(f"成功:{app_url}")
        p=[["成功",t]]
    else:
        st.write(f"失败:{app_url}")
        p=[["失败",t]]

    newdf = pd.DataFrame(p,columns=["消息","时间"])
    df = pd.concat([df,newdf],ignore_index=False)
    df.to_csv(file)

# 设置定期访问的时间间隔（以秒为单位）
interval = random.randint(3600*12, 3600*15)  # 每12H访问一次

while True:
    time.sleep(interval)
    keep_alive()
