import streamlit as st
from PIL import Image
import numpy as np
from openai import OpenAI

img_file_buffer = st.camera_input("点击拍照1")

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



if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    img_array = np.array(img)
    ai("分析这个图像显示的内容",1,"你是一个图像分析师")
    #st.write(type(img_array))
    #st.write(img_array.shape)
    
    
    
