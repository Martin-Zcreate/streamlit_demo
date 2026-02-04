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
    
    # 建立连接 (已修复URL格式)
    client = OpenAI(
        api_key=a,
        base_url="https://api.siliconflow.cn/v1"
    )

    try:
        # 读取图片并转为 Base64
        c = uploaded_file.getvalue()
        d = base64.b64encode(c).decode('utf-8')
        
        print(f"正在发送请求给模型: {b} ...")

        e = client.chat.completions.create(
            model=b,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请将这张图片里的所有文字和数学公式提取出来，公式请使用 LaTeX 格式。"},
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
    # 建立连接 (已修复URL格式)
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
              4. 公式请使用markdown格式。
             """
             },
            {"role": "user", "content": f"学生发来了这道题，请讲解：\n{question_text}"},
        ],
        stream=True
    )
    return response

# ================= 网页界面布局 =================

st.title("🤖智酷AI作业帮手")

# 核心修改：优先展示摄像头输入
method = st.radio("选择输入方式", ["📸 拍照", "📤 上传图片"], horizontal=True)

img_file = None

if method == "📸 拍照":
    # camera_input 会在移动端浏览器请求摄像头权限并直接显示画面
    img_file = st.camera_input("点击下方按钮拍照")
else:
    img_file = st.file_uploader(
        "选择作业图片", 
        type=['jpg', 'png', 'jpeg'], 
        accept_multiple_files=False
    )

if img_file:
    with st.spinner('正在识别题目...'):
        f = get_ocr_text(img_file)

    if f:
        st.subheader("📝 识别到的题目")
        st.info(f)
        
        st.subheader("👨‍🏫 老师讲解")
        result_area = st.empty()
        
        g = AI(f)
        
        full_response = ""
        for chunk in g:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                result_area.markdown(full_response)
