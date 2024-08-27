import streamlit as st

st.title("梁友嘉的个人网页😭")
st.title("音乐😇")
m = st.selectbox("选择音乐",("少年","夜曲"))
                 
a = open(f"music1/{m}.mp3","rb").read()
st.audio(a)
st.image(f"picture1/{m}.jpg")

st.title("电影🎃")
movie = st.multiselect("选择电影",("飞驰人生","流浪地球"))
                       
for i in movie:
    st.image(f"picture1/{i}.jpg")
