import requests
import base64
from openai import OpenAI
import streamlit as st 
from PIL import Image
import numpy as np

st.set_page_config(page_title="数学解题AI",layout="wide",page_icon="🙃" )

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
你是一个专业的高中数学老师，你的工作是辅导高一学生的理解并做出数学题目,
你需要做以下事情：
1.讲解题目的思路。
2.通俗易懂的方式如何理清解题思路。
3.给出有解题过程的答案，尽量详细。
"""
s=''
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

img_file_buffer = st.camera_input("点击拍照")
if img_file_buffer is not None:
    imag = Image.open(img_file_buffer)
    pic = imag.save('123.png', 'PNG')

    f = open('123.png', 'rb')
    img = base64.b64encode(f.read())
    
    params = {"image":img}
    access_token = '24.2c2db58f2d82deb5596706316b5342a8.2592000.1721465622.282335-84920272'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        for i in response.json()['words_result']:
            s+=i['words']
        st.write(s)
        ai(s,0,pro)
