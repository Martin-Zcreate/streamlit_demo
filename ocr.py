import streamlit as st
import base64
from openai import OpenAI

def get_img_str(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_ocr_text(uploaded_file):
    a = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr"
    b = "deepseek-ai/DeepSeek-OCR" 

    # 建立连接 (硅基流动专用地址)
    client = OpenAI(
        api_key=a, 
        base_url="https://api.siliconflow.cn/v1"
    )

    # 辅助函数：把图片转成字符串
    

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
                        {"type": "text", "text": "请将这张图片里的所有文字和数学公式提取出来，公式请使用 LaTeX 格式。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{d}"}}
                    ]
                }
            ],
            temperature=0.1, # 0.1 让它严谨点，别乱发挥
        )

        # 打印结果

        return e.choices[0].message.content

    except Exception as err:
        st.error(f"OCR出错: {e}")
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
              1. 当学生问问题时，不要直接给完整代码或答案。
              2. 请使用"难度降级"法，把复杂的题目拆解成简单的步骤。
              3. 如果是编程题，先解释思路，再让学生去思考代码。
              4. 公式请使用 LaTeX 格式。
             """
             
             },
            {"role": "user", "content": f"学生发来了这道题，请讲解：\n{question_text}"},
        ],
        stream=True
    )
    return response 

# ================= 网页界面布局 =================

st.title("🤖 AI 作业帮手")
st.write("用手机拍下题目，AI 帮你拆解思路。")

# 1. 手机调用摄像头组件
img_file = st.file_uploader(
    "📸 点击拍摄题目 (或在左侧选择其他功能)", 
    type=['jpg', 'png', 'jpeg'], 
    accept_multiple_files=False,
    key="uploader"
)

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
