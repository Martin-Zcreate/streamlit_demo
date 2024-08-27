import streamlit as st

st.title("刘晨鑫的个人网站🤡")
st.title("音乐")
m = st.selectbox("选择音乐",("夜曲","少年","天空之城","夜空中最亮的星"))

a = open(f"music1/{m}.mp3","rb").read()
st.audio(a)
st.image(f"picture1/{m}.jpg")

st.title("电影")
movie = st.multiselect("选择电影",("飞驰人生","流浪地球"))
for i in movie:
    st.image(f"picture1/{i}.jpg")
