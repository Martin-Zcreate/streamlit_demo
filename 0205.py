import cv2
import numpy as np
import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from cvzone.HandTrackingModule import HandDetector

# --- 页面设置 ---
st.set_page_config(page_title="云端AI神笔", layout="wide")
st.title("🖐️ 云端版 AI 神笔马良")
st.info("提示：请允许浏览器访问摄像头。首次加载可能需要 10-20 秒。")

# --- 定义画笔参数 ---
# 注意：在WebRTC运行时，实时修改侧边栏参数比较复杂，
# 为了演示稳定，我们把参数固定或简化
draw_color = (0, 255, 0) # 绿色 (B, G, R)
brush_thickness = 15

# --- 核心处理类 ---
# 这里不再是用 while 循环，而是定义一个“处理器”
class HandTrackProcessor(VideoTransformerBase):
    def __init__(self):
        # 初始化手部检测器
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        # 初始化画布 (Canvas)
        # 注意：这里不能确定摄像头分辨率，先设为None，第一帧来了再创建
        self.canvas = None
        # 上一帧的坐标点
        self.xp, self.yp = 0, 0

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """
        这个函数会针对每一帧视频被调用一次
        """
        # 1. 把来自网络的帧转换为 OpenCV 图像格式
        img = frame.to_ndarray(format="bgr24")
        
        # 翻转镜像
        img = cv2.flip(img, 1)
        
        # 2. 初始化画布（如果还没创建）
        if self.canvas is None:
            # 创建一个和当前视频帧一样大小的黑底画布
            self.canvas = np.zeros_like(img)

        # 3. AI手部识别
        hands, img = self.detector.findHands(img, flipType=False, draw=True)

        if hands:
            lmList = hands[0]['lmList']
            # 食指指尖(8) 和 中指指尖(12)
            x1, y1 = lmList[8][0], lmList[8][1]
            x2, y2 = lmList[12][0], lmList[12][1]

            # 判断手指状态
            fingers = self.detector.fingersUp(hands[0])

            # --- 逻辑复用之前的 ---
            # 模式A：暂停 (食指+中指)
            if fingers[1] and fingers[2]:
                self.xp, self.yp = 0, 0
                cv2.circle(img, (x1, y1), 25, draw_color, cv2.FILLED)

            # 模式B：绘画 (仅食指)
            elif fingers[1] and not fingers[2]:
                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = x1, y1
                
                # 在 self.canvas 上画线
                cv2.line(self.canvas, (self.xp, self.yp), (x1, y1), draw_color, brush_thickness)
                self.xp, self.yp = x1, y1

        # 4. 图像融合 (把画布叠加到摄像头画面)
        imgGray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, self.canvas)

        # 5. 把处理好的 OpenCV 图像转回 WebRTC 帧返回给浏览器
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 启动 WebRTC 组件 ---
# rtc_configuration 用于配置穿透服务器(STUN/TURN)，
# 在某些公司内网或校园网可能因为防火墙无法连接，
# 这里使用 Google 免费的 STUN 服务器尝试连接。
rtc_configuration = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
}

webrtc_streamer(
    key="hand-drawing",
    video_processor_factory=HandTrackProcessor,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={"video": True, "audio": False}, # 只要视频，不要音频
)

st.markdown("---")
st.write("操作说明：")
st.write("1. 点击 START 按钮开启摄像头。")
st.write("2. 伸出**食指**进行绘画。")
st.write("3. 同时伸出**食指和中指**暂停绘画。")
st.write("4. 点击 STOP 再点击 START 可以清空画布。")
