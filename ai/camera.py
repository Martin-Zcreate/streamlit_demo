import streamlit as st

picture = st.camera_input("点击拍照")

if picture:
    st.image(picture)
