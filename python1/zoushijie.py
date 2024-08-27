import streamlit as st

st.title("邹世杰的个人网站 Hi~ o(*￣▽￣*)ブ")

st.title("音乐🧿")
m = st.selectbox("选择你喜欢的音乐",("夜曲","少年","天空之城","夜空中最亮的星"))
a = open(f"music1/{m}.mp3","rb").read()
st.audio(a)
st.image(f"picture1/{m}.jpg")

st.title("电影📽")
n = st.multiselect("选择你喜欢的电影",("飞驰人生","流浪地球","复仇者联盟","猩球崛起"))
for i in n:
    st.image(f"picture1/{i}.jpg")
