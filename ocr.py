import streamlit as st
import base64
from openai import OpenAI
from PIL import Image

def get_img_str(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_ocr_text(uploaded_file):
    a = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr"
    b = "deepseek-ai/DeepSeek-OCR"
    
    # 建立连接
    client = OpenAI(
        api_key=a,
        base_url="https://api.siliconflow.cn/v1"
    )

    try:
        # d: 图片的 Base64 编码
        c = uploaded_file.getvalue()
        d = base64.b64encode(c).decode('utf-8')
        
        print(f"正在发送请求给模型: {b} ...")

        # e: 发送请求
        e = client.chat.completions.create(
            model=b,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请将这张图片里的所有文字和数学公式提取出来，公式请使用 markdown 格式。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{d}"}}
                    ]
                }
            ],
            temperature=0.1,
        )

        return e.choices[0].message.content

    except Exception as err:
        st.error(f"OCR出错: {err}")
        return None


def AI(question_text):
    client = OpenAI(api_key="sk-af6ba48dbd8a4d1fb0d036551b9bbdc3",
                    base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": 
             """
              你是一位专业的老师。
              1. 当学生问问题时，不要直接给完整答案。
              2. 请使用"难度降级"法，把复杂的题目拆解成简单的步骤。
              3. 先解释思路，再让学生去思考问题。
              4. 写出答案,具体讲解下.
              5. 公式请使用markdown格式。
             """
             },
            {"role": "user", "content": f"学生发来了这道题，请讲解：\n{question_text}"},
        ],
        stream=True
    )
    return response

# ================= 网页界面布局 =================

st.set_page_config(page_title="智酷AI作业帮手", page_icon="🤖")
st.title("🤖智酷AI作业帮手")

# 错误处理提示
if "webrtc_failed" not in st.session_state:
    st.session_state.webrtc_failed = False

st.info("💡 提示：为保证最佳识别效果，请优先使用【系统相机】拍摄清晰照片。")

# 选项卡布局
tab1, tab2 = st.tabs(["📱 系统相机 (推荐)", "  网页相机 (备用)"])

img_file = None

with tab1:
    st.markdown("### 📷 调用手机原生相机")
    st.markdown("""
    <style>
    /* 尝试通过 CSS 引导用户 */
    div[data-testid="stFileUploader"] label {
        font-size: 1.2rem !important;
        color: #FF4B4B !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("点击下方按钮，直接选择 **“拍照”** 或 **“相机”**。")
    
    img_file_upload = st.file_uploader(
        "🔴 点这里 -> 选择 '拍照'", 
        type=['jpg', 'png', 'jpeg'], 
        accept_multiple_files=False,
        key="uploader"
    )
    if img_file_upload:
        img_file = img_file_upload

with tab2:
    st.markdown("### 💻 网页直接抓拍")
    st.caption("注意：此模式在部分安卓/iOS设备上可能无法对焦，仅建议电脑端使用。")
    img_file_camera = st.camera_input("点击拍摄", key="camera")
    if img_file_camera:
        img_file = img_file_camera

if img_file:
    # 显示个加载圈
    with st.spinner('正在识别题目...'):
        # f: 识别出的文字
        f = get_ocr_text(img_file)

    if f:
        # 显示识别结果给用户确认
        st.subheader("📝 识别到的题目")
        st.info(f)
        
        # 开始讲解
        st.subheader("👨‍🏫 老师讲解")
        result_area = st.empty() # 创建一个空位用来打字
        
        # g: 接收流式回复
        g = AI(f)
        
        # 拼接回复
        full_response = ""
        for chunk in g:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                result_area.markdown(full_response) # 实时更新屏幕
