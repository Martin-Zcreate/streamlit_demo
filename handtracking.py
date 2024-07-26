import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import Image,ImageDraw,ImageFont

def text(img,t,p,path,size,color):
    pil=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw=ImageDraw.Draw(pil)
    font=ImageFont.truetype(path,size)
    draw.text(p,t,font=font,fill=color)
    cv=cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)
    return cv 

st.title("实时视频流示例")

# 捕获视频流
cap = cv2.VideoCapture(0)

d = HandDetector(maxHands=1, detectionCon=0.8)
# 创建一个占位符来显示视频帧
video_placeholder = st.empty()
x="请放上手掌"
while 1:
    # 读取帧
    success, frame = cap.read()
    # 将帧从 BGR 转换为 RGB
    hands, frame_rgb = d.findHands(frame,draw=1)
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    if hands:
        hand1 = hands[0]
        f = d.fingersUp(hand1)
        if f==[0,1,0,0,0]:
            x='1'
        elif f==[0,1,1,0,0]:
            x="2"
        elif f==[0,1,1,1,0]:
            x="3"
        elif f==[0,1,1,1,1]:
            x="4"
        elif f==[1,1,1,1,1]:
            x="5"
        elif f==[1,0,0,0,1]:
            x="6"
        elif f==[1,1,1,0,0]:
            x="7"
        elif f==[1,1,0,0,0]:
            x="8"
        elif f==[0,0,0,0,0]:
            x="0"
        elif f==[0,0,1,1,1]:
            x="OK"
        else:   
            x="无"
    else:
        x="请放上手掌"
    
    # 显示帧
    frame_rgb=text(frame_rgb,x,(30,30),"simhei.ttf",90,(255,0,0))
    video_placeholder.image(frame_rgb, channels="RGB")

    # 控制帧率
    #time.sleep(0.03)  # 大约 30 FPS

# 释放视频捕获对象
cap.release()
