import streamlit as st
import datetime
import os

# 检查是否存在留言记录文件，如果不存在则创建一个空列表
if not os.path.exists('comments.txt'):
    with open('comments.txt', 'w') as file:
        file.write('')

# 读取留言记录文件
with open('comments.txt', 'r') as file:
    comments = file.readlines()

# 留言板界面
st.title('留言板')

# 提交留言的表单
name = st.text_input('输入你的姓名:')
comment = st.text_input('留下你的消息:')
submit = st.button('提交')

# 如果用户点击了提交按钮
if submit:
    # 获取当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # 创建留言内容，包括时间戳和用户留言
    new_comment = f"{name} : {comment}--{current_time}\n"
    # 将新留言追加到文件
    with open('comments.txt', 'a+') as file:
        file.write(new_comment)
    # 清空输入框
    st.success('留言已提交！')
    file.close()

# 展示留言
st.header('历史留言')
for comment in comments:
    user_write = st.chat_message("user")
    user_write.write(comment.strip())



    
  
