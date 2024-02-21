import streamlit as st 
import numpy as np

st.title("NO.1 年龄😄")
a1 = st.checkbox('输入年龄')
if a1:
    age = st.slider('你多大啦?', 0, 130, 25)
    st.write(f"我今年{age}岁")

st.title("NO.2 最爱看的电影📽")
a2 = st.checkbox('开始选电影')
if a2:
    movie = st.multiselect(
        '选择你喜欢的电影吧！',
        ['星际穿越', '猩球崛起', '复仇者联盟', '流浪地球','洛奇', '飞驰人生'],
        ['洛奇', '飞驰人生'])
    st.write(f'你喜欢看{movie}这些电影')

st.title("NO.3 喜欢听的音乐🎵")
a3 = st.checkbox('开始选音乐')
if a3:
    music = st.selectbox(
    '选择你喜欢的音乐',
    ('夜曲','夜空中最亮的星','天空之城'))
    if music:
        audio_file = open(f'music1/{music}.mp3', 'rb')
        audio_bytes = audio_file.read()
        
        sample_rate = 44100  # 44100 samples per second
        st.audio(audio_bytes)
    
