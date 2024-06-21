import streamlit as st
from PIL import Image
import numpy as np

# 页面标题
st.title('留言板应用')

# 留言板页面
st.title('留言板')

# 上传视频
video_file = st.file_uploader("上传视频", type=["mp4", "mov", "avi"])
if video_file is not None:
    st.video(video_file)

# 上传图片
image_file = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
if image_file is not None:
    img = Image.open(image_file)
    img_array = np.array(img)
    st.image(img_array, caption='上传的图片', use_column_width=True)

# 留言
message = st.text_area("留言")
if st.button("提交留言"):
    if message:
        st.success("留言已提交")
    else:
        st.warning("请输入留言内容")
