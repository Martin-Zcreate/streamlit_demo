import streamlit as st
from PIL import Image
import numpy as np
import os
import csv

# 初始化CSV文件
def init_csv():
    if not os.path.exists('messages.csv'):
        with open('messages.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "message", "video_path", "image_path"])

# 保存留言信息到CSV文件
def save_message(message, video_path=None, image_path=None):
    with open('messages.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([None, message, video_path, image_path])

# 从CSV文件中获取所有留言信息
def get_messages():
    with open('messages.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        messages = list(reader)
    return messages

# 初始化CSV文件
init_csv()

# 页面标题
st.title('留言板应用')

# 留言板页面
st.title('留言板')

# 上传视频
video_file = st.file_uploader("上传视频", type=["mp4", "mov", "avi"])
video_path = None
if video_file is not None:
    os.makedirs("videos", exist_ok=True)  # 确保视频目录存在
    video_path = f"videos/{video_file.name}"
    with open(video_path, "wb") as f:
        f.write(video_file.getbuffer())
    st.video(video_path)

# 上传图片
image_file = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
image_path = None
if image_file is not None:
    os.makedirs("images", exist_ok=True)  # 确保图片目录存在
    image_path = f"images/{image_file.name}"
    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())
    img = Image.open(image_file)
    img_array = np.array(img)
    st.image(img_array, caption='上传的图片', use_column_width=True)

# 留言
message = st.text_area("留言")
if st.button("提交留言"):
    if message:
        save_message(message, video_path, image_path)
        st.success("留言已提交")
    else:
        st.warning("请输入留言内容")

# 显示所有留言信息
messages = get_messages()
for msg in messages:
    st.write(f"留言: {msg[1]}")
    if msg[2]:
        st.video(msg[2])
    if msg[3]:
        st.image(msg[3])
