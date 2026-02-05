import streamlit as st
import base64
import re
import io
import json
from PIL import Image, ImageOps
from openai import OpenAI

# ================= 配置区域 =================
# ⚠️ 填入你的 Key
API_KEY = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr" 
OCR_MODEL = "deepseek-ai/DeepSeek-OCR"
CHAT_MODEL = "deepseek-ai/DeepSeek-V3"

# ================= 核心工具 =================

def clean_latex(text):
    """
    清洗数据：处理 LaTeX 符号，同时防止模型返回 JSON 格式导致满屏大括号
    """
    if not text:
        return ""

    # 1. 🔍 防错：如果模型返回了 JSON 格式 (例如 {"content": "..."})，尝试提取内部文本
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        try:
            data = json.loads(text)
            # 尝试找常见的字段名
            if "content" in data: text = data["content"]
            elif "text" in data: text = data["text"]
        except:
            pass # 解析失败就算了，按原样处理

    # 2. 🧹 移除 Markdown 代码块包裹 (```json 或 ```latex)
    text = re.sub(r'^```\w*\n', '', text) # 去头
    text = re.sub(r'\n```$', '', text)    # 去尾

    # 3. 📐 修正公式格式
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
    
    return text

def process_image(image_bytes, max_mb=4):
    """图片预处理：修正旋转 + 智能压缩"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = ImageOps.exif_transpose(img) # 修正手机拍照旋转
        
        # 修复透明底变黑
        if img.mode != 'RGB':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if 'A' in img.mode or 'transparency' in img.info:
                img = img.convert('RGBA')
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert('RGB')

        # 压缩逻辑
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        
        # 只有在图片真的很大 (>4MB) 时才压缩
        if len(buf.getvalue()) > max_mb * 1024 * 1024:
            img.save(buf, format="JPEG", quality=85) # 稍微降点质量即可
            
        return buf.getvalue()
    except Exception as e:
        st.error(f"图片处理出错: {e}")
        return image_bytes

def get_ocr_text(image_bytes):
    """调用 OCR，代码结构已拆解，防止括号报错"""
    client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")

    try:
        # 1. 准备 Base64 字符串
        b64_str = base64.b64encode(image_bytes).decode('utf-8')
        
        # 2. 准备消息内容 (拆开写，不套娃)
        text_part = {"type": "text", "text": "提取图中所有文字和LaTeX公式。直接输出内容，不要包含JSON格式或Markdown代码块。"}
        image_part = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64_str}",
                "detail": "high" # 👈 关键：强制高清
            }
        }
        
        # 3. 发送请求
        response = client.chat.completions.create(
            model=OCR_MODEL,
            messages=[{"role": "user", "content": [text_part, image_part]}],
            temperature=0.0,
            top_p=0.7,
            max_tokens=4096
        )
        
        return clean_latex(response.choices[0].message.content)

    except Exception as e:
        st.error(f"OCR 请求失败: {e}")
        return None

def ai_stream(history):
    """调用对话模型"""
    client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")
    
    # 只发送文本给对话模型，避免发图片报错
    clean_history = []
    for msg in history:
        clean_history.append({"role": msg["role"], "content": str(msg["content"])})

    return client.chat.completions.create(
        model=CHAT_MODEL,
        messages=clean_history,
        stream=True,
        temperature=0.7
    )

# ================= 网页主程序 =================

st.set_page_config(page_title="AI 题目讲解", layout="centered")
st.title("🎓 AI 题目讲解助手")

if "history" not in st.session_state:
    st.session_state.history = []
if "last_file_id" not in st.session_state:
    st.session_state.last_file_id = None

uploaded_file = st.file_uploader("📸 上传题目图片", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    file_id = f"{uploaded_file.name}-{uploaded_file.size}"
    
    # 新图片处理流程
    if st.session_state.last_file_id != file_id:
        st.session_state.last_file_id = file_id
        st.session_state.history = []
        
        with st.status("🚀 正在识别题目...", expanded=True) as status:
            # 1. 处理图片
            img_bytes = process_image(uploaded_file.getvalue())
            # 2. 识别文字
            ocr_result = get_ocr_text(img_bytes)
            
            if ocr_result:
                status.update(label="识别成功！", state="complete", expanded=False)
                
                # 初始化对话
                sys_msg = "你是一位老师。请解析题目思路，公式使用LaTeX格式($...$ 或 $$...$$)。"
                user_msg = f"题目内容如下：\n{ocr_result}\n\n请讲解。"
                
                st.session_state.history = [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg}
                ]
                
                # 自动触发讲解
                with st.chat_message("assistant"):
                    ph = st.empty()
                    full_text = ""
                    try:
                        for chunk in ai_stream(st.session_state.history):
                            if chunk.choices[0].delta.content:
                                full_text += chunk.choices[0].delta.content
                                ph.markdown(clean_latex(full_text) + "▌")
                        ph.markdown(clean_latex(full_text))
                        st.session_state.history.append({"role": "assistant", "content": full_text})
                    except Exception as e:
                        st.error(f"讲解出错: {e}")
            else:
                status.update(label="识别失败", state="error")

# 显示历史对话
for msg in st.session_state.history:
    if msg["role"] != "system":
        # 这里的判断是为了不重复显示第一条很长的题目内容，保持界面清爽
        # 如果你想看题目，就把下面这两行删掉
        if "题目内容如下" in str(msg["content"]) and msg["role"] == "user":
            with st.expander("查看识别到的题目"):
                st.markdown(clean_latex(msg["content"]))
            continue
            
        with st.chat_message(msg["role"]):
            st.markdown(clean_latex(msg["content"]))

# 输入框
if query := st.chat_input("哪里不懂？"):
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.history.append({"role": "user", "content": query})
    
    with st.chat_message("assistant"):
        ph = st.empty()
        full_text = ""
        try:
            for chunk in ai_stream(st.session_state.history):
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    ph.markdown(clean_latex(full_text) + "▌")
            ph.markdown(clean_latex(full_text))
            st.session_state.history.append({"role": "assistant", "content": full_text})
        except Exception as e:
            st.error(f"出错: {e}")
