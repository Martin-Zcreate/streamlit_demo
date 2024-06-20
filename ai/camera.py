import requests
import base64
from openai import OpenAI
import streamlit as st 
from PIL import Image
import numpy as np


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

pro = """
你是一名专业的高中语文老师,你可以辅导学生完成作业,给出思路过程,并给出答案。
"""
s=''
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# 二进制方式打开图片文件
img_file_buffer = st.camera_input("点击拍照")
if img_file_buffer is not None:
    img = Image.open(img_file_buffer).tobytes()

    # f = open('C:/Users/z/streamlitdemo/123.png', 'rb')
    # img = base64.b64encode(imag.read())
    
    params = {"image":img}
    access_token = '24.2c2db58f2d82deb5596706316b5342a8.2592000.1721465622.282335-84920272'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        s = response.json()
        write(s)
        ai(s,pro,1)
