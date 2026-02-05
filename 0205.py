import cv2
import numpy as np
import streamlit as st
from cvzone.HandTrackingModule import HandDetector

# --- 1. 页面配置 ---
st.set_page_config(page_title="AI神笔马良", layout="wide")

# --- 2. 初始化核心变量 (关键步骤) ---
# Streamlit每帧都会刷新代码，必须把画布存在 session_state 里，否则一刷新画的画就没了
if 'canvas' not in st.session_state:
    # 创建一个全黑的图层，尺寸 1280x720 (根据摄像头调整)
    st.session_state.canvas = np.zeros((720, 1280, 3), np.uint8)

# --- 3. 侧边栏控制台 ---
st.sidebar.title("🎨 控制台")
# 让观众选颜色，增加互动
hex_color = st.sidebar.color_picker('画笔颜色', '#00FF00') 
# 把十六进制颜色转成 OpenCV 的 BGR 格式
r = int(hex_color[1:3], 16)
g = int(hex_color[3:5], 16)
b = int(hex_color[5:7], 16)
draw_color = (b, g, r) # OpenCV用的是BGR顺序

brush_thickness = st.sidebar.slider('画笔粗细', 5, 50, 15)
if st.sidebar.button('🗑️ 清空画布'):
    st.session_state.canvas = np.zeros((720, 1280, 3), np.uint8)

# --- 4. 摄像头与AI初始化 ---
st.title("🖐️ Python AI 隔空手势画板")
st.caption("食指：写字 | 食指+中指：暂停")
# 创建一个空白组件，后面在这个位置不断刷图
frame_window = st.image([]) 

cap = cv2.VideoCapture(0)
# 设置摄像头分辨率，越大越清晰，但对电脑性能要求越高
cap.set(3, 1280) 
cap.set(4, 720)

# detectionCon=0.8 表示AI要有80%把握才认为是手，防抖动
detector = HandDetector(detectionCon=0.8, maxHands=1)

# 记录上一帧的指尖坐标，用来画连续的线
xp, yp = 0, 0 

# --- 5. 主循环 (直播演示核心) ---
run = st.checkbox('开启摄像头', value=True)

while run:
    success, img = cap.read()
    if not success: break
    
    # 镜像翻转，不然左右是反的，操作很别扭
    img = cv2.flip(img, 1) 
    
    # 【AI核心】寻找手部关键点
    hands, img = detector.findHands(img, flipType=False, draw=True)
    
    if hands:
        lmList = hands[0]['lmList'] # 获取21个关节坐标列表
        # 获取 食指指尖(8) 和 中指指尖(12) 的坐标
        x1, y1 = lmList[8][0], lmList[8][1]
        x2, y2 = lmList[12][0], lmList[12][1]
        
        # 判断手指是不是竖起来了 (返回一个列表 [0,1,1,0,0] 这种)
        fingers = detector.fingersUp(hands[0])
        
        # 模式A：食指和中指都竖起来 -> 【暂停/移动模式】
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0 # 重置坐标，断开线条
            cv2.circle(img, (x1, y1), 25, draw_color, cv2.FILLED) # 画个大点提示暂停
            
        # 模式B：只有食指竖起来 -> 【绘画模式】
        elif fingers[1] and not fingers[2]:
            # 如果是刚开始画，就把起点设为当前点
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            
            # 在“虚拟画布”上画线
            cv2.line(st.session_state.canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
            xp, yp = x1, y1 # 更新坐标

    # --- 6. 图像融合 (最难理解的部分) ---
    # 简单说：把黑底彩线的画布，像贴纸一样贴到摄像头画面上
    
    # 步骤A：把画布变成灰度图
    imgGray = cv2.cvtColor(st.session_state.canvas, cv2.COLOR_BGR2GRAY)
    # 步骤B：做一个反向遮罩 (黑线白底)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    
    # 步骤C：把摄像头画面中，要画线的地方“抠黑”
    img = cv2.bitwise_and(img, imgInv)
    # 步骤D：把画布里的颜色填进去
    img = cv2.bitwise_or(img, st.session_state.canvas)

    # --- 7. 显示画面 ---
    # OpenCV是BGR，网页显示要RGB，转一下
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_window.image(imgRGB)

cap.release()
