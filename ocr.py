import streamlit as st
import base64
import re
import io
from PIL import Image
from openai import OpenAI

def clean_latex(text):
    """
    将 LaTeX 的 \( ... \) 转换为 $ ... $
    将 \[ ... \] 转换为 $$ ... $$
    以便 Streamlit 正确渲染
    """
    if not text:
        return text
    # 替换块级公式 \[ ... \] 为 $$ ... $$
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    # 替换行内公式 \( ... \) 为 $ ... $
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
    return text

def compress_image(image_bytes, max_size_kb=150):
    """
    如果图片超过 max_size_kb，则进行压缩
    """
    try:
        current_size = len(image_bytes)
        if current_size <= max_size_kb * 1024:
            return image_bytes

        st.toast(f"图片大小 {current_size/1024:.1f}KB > {max_size_kb}KB，正在压缩...", icon="📉")
        
        img = Image.open(io.BytesIO(image_bytes))
        
        # 转换为 RGB (兼容 PNG/RGBA)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # 循环压缩直到满足大小
        quality = 90
        width, height = img.size
        scale = 1.0
        
        while True:
            output_buffer = io.BytesIO()
            # 调整尺寸
            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                resized_img.save(output_buffer, format="JPEG", quality=quality)
            else:
                img.save(output_buffer, format="JPEG", quality=quality)
            
            compressed_bytes = output_buffer.getvalue()
            
            if len(compressed_bytes) <= max_size_kb * 1024:
                return compressed_bytes
            
            # 如果还是太大，降低质量或尺寸
            if quality > 60:
                quality -= 10
            else:
                # 质量已经很低了，开始缩尺寸
                scale *= 0.8
                
            # 避免死循环
            if scale < 0.1:
                return compressed_bytes

    except Exception as e:
        st.warning(f"图片压缩异常: {e}")
        return image_bytes

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
        raw_bytes = uploaded_file.getvalue()
        
        # 压缩处理 (如果 > 150KB)
        processed_bytes = compress_image(raw_bytes, max_size_kb=150)
        
        d = base64.b64encode(processed_bytes).decode('utf-8')
        
        print(f"正在发送请求给模型: {b} ...")

        # e: 发送请求
        e = client.chat.completions.create(
            model=b,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请将这张图片里的所有文字和数学公式提取出来。公式请使用 LaTeX 格式，行内公式用 $ 包裹，独立公式用 $$ 包裹。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{d}"}}
                    ]
                }
            ],
            temperature=0.1, # 0.1 让它严谨点，别乱发挥
        )

        # 打印结果

        content = e.choices[0].message.content
        return clean_latex(content)

    except Exception as err:
        st.error(f"OCR出错: {err}")
        return None


def AI_stream(messages):
    client = OpenAI(api_key="sk-af6ba48dbd8a4d1fb0d036551b9bbdc3",
                    base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )
    return response

# ================= 网页界面布局 =================

st.title("🤖 AI 作业帮手")
st.write("用手机拍下题目，AI 帮你拆解思路。")

# 初始化 Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
if "ocr_result" not in st.session_state:
    st.session_state.ocr_result = None

# 系统提示词
SYSTEM_PROMPT = """
你是一位专业的老师。
1. 当学生问问题时，不要直接给完整代码或答案。
2. 请使用"难度降级"法，把复杂的题目拆解成简单的步骤。
3. 如果是编程题，先解释思路，再让学生去思考代码。
4. 公式请使用 LaTeX 格式，行内公式用 $ 包裹，独立公式用 $$ 包裹。
"""

# 1. 手机调用摄像头组件
img_file = st.file_uploader(
    "📸 点击拍摄题目 (或在左侧选择其他功能)", 
    type=['jpg', 'png', 'jpeg'], 
    accept_multiple_files=False,
    key="uploader"
)

if img_file:
    # 生成文件指纹 (简单用 name + size)
    file_id = f"{img_file.name}-{img_file.size}"
    
    # 如果是新文件，重置状态
    if st.session_state.last_uploaded_file != file_id:
        st.session_state.last_uploaded_file = file_id
        st.session_state.messages = []
        st.session_state.ocr_result = None
        
        # 执行 OCR
        with st.spinner('正在识别题目...'):
            st.session_state.ocr_result = get_ocr_text(img_file)

    # 如果有识别结果
    if st.session_state.ocr_result:
        f = st.session_state.ocr_result
        
        # 显示识别结果给用户确认
        st.subheader("📝 识别到的题目")
        st.markdown(f)
        
        # ----------------- 对话区域 -----------------
        st.subheader("👨‍🏫 老师讲解 & 答疑")
        
        # 如果历史为空，说明是刚识别完，自动触发第一次讲解
        if not st.session_state.messages:
            initial_user_msg = f"学生发来了这道题，请讲解：\n{f}"
            
            # 存入第一条用户消息（但不在界面上重复显示，因为上面已经显示了题目）
            st.session_state.messages.append({"role": "user", "content": initial_user_msg})
            
            # 构造 API 请求消息
            api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            
            # 显示 AI 回复容器
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 调用 AI
                try:
                    stream = AI_stream(api_messages)
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(clean_latex(full_response))
                    
                    # 存入历史
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"AI 响应出错: {e}")

        else:
            # 如果已有历史，渲染历史消息
            for i, msg in enumerate(st.session_state.messages):
                # 跳过第一条 User 消息（因为它是题目，已经显示在上面了）
                if i == 0 and msg["role"] == "user":
                    continue
                
                with st.chat_message(msg["role"]):
                    st.markdown(clean_latex(msg["content"]))

        # ----------------- 底部输入框 -----------------
        if prompt := st.chat_input("还有哪里不懂？继续问老师..."):
            # 1. 显示用户输入
            with st.chat_message("user"):
                st.markdown(prompt)
            # 存入历史
            st.session_state.messages.append({"role": "user", "content": prompt})

            # 2. 生成 AI 回复
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 构造 API 请求
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                
                try:
                    stream = AI_stream(api_messages)
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(clean_latex(full_response))
                    
                    # 存入历史
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"AI 响应出错: {e}")
