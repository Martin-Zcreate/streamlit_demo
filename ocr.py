import streamlit as st
import base64
import re
import io
import json
from PIL import Image, ImageOps
from openai import OpenAI

# ================= 恢复你的 API KEY =================
# 硅基流动 Key (用于 OCR) - 对应你提供的第一个 Key
OCR_API_KEY = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr"
# DeepSeek Key (用于对话) - 对应你提供的第二个 Key
CHAT_API_KEY = "sk-af6ba48dbd8a4d1fb0d036551b9bbdc3"

# ================= 核心清洗工具 (解决花括号问题) =================

def clean_text(text):
    """
    终极清洗函数：
    1. 去除 JSON 花括号包裹
    2. 去除 Markdown 代码块
    3. 修复 LaTeX 格式
    """
    if not text:
        return ""

    text = text.strip()

    # --- 1. 暴力去除 JSON 外壳 ---
    # 如果内容以 ```json 开头，或者以 { 开头，尝试解析
    if text.startswith("```") or text.startswith("{"):
        # 移除 markdown 标记
        text = re.sub(r'^```(json)?', '', text, flags=re.MULTILINE)
        text = re.sub(r'```$', '', text, flags=re.MULTILINE)
        text = text.strip()
        
        # 尝试作为 JSON 解析
        try:
            data = json.loads(text)
            # 如果解析成功，优先取 'content' 或 'text' 字段
            if isinstance(data, dict):
                if "content" in data:
                    text = data["content"]
                elif "text" in data:
                    text = data["text"]
                # 如果是其他 key，比如 {"result":...}, 只要是字典且只有一个大 value，就取那个
                elif len(data) == 1:
                    text = list(data.values())[0]
        except:
            # 如果解析失败（比如 JSON 不完整），尝试用正则提取 content":"..." 后面的内容
            match = re.search(r'"content"\s*:\s*"(.*?)"', text, re.DOTALL)
            if match:
                text = match.group(1)
                # 处理转义字符
                text = text.replace('\\n', '\n').replace('\\"', '"')

    # --- 2. 修复 LaTeX 格式 ---
    # 将 \[ \] 替换为 $$
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    # 将 \( \) 替换为 $
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
            img.save(buf, format="JPEG", quality=85) 
            
        return buf.getvalue()
    except Exception as e:
        st.error(f"图片处理出错: {e}")
        return image_bytes

def get_ocr_text(image_bytes):
    """调用 OCR，加入 JSON 禁用提示"""
    # 使用硅基流动 Key
    client = OpenAI(api_key=OCR_API_KEY, base_url="https://api.siliconflow.cn/v1")

    try:
        b64_str = base64.b64encode(image_bytes).decode('utf-8')
        
        # 提示词：明确要求不要输出 JSON
        prompt_text = "提取图中所有文字和公式。请直接输出纯文本内容，不要输出 JSON 格式，不要使用代码块包裹。"
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-OCR",
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_str}",
                                "detail": "high" # 强制高清
                            }
                        }
                    ]
                }
            ],
            temperature=0.0, # 严谨模式
            max_tokens=4096
        )
        
        raw_content = response.choices[0].message.content
        return clean_text(raw_content)

    except Exception as e:
        st.error(f"OCR 请求失败: {e}")
        return None

def ai_stream(history):
    """调用对话模型"""
    # 使用 DeepSeek Key
    client = OpenAI(api_key=CHAT_API_KEY, base_url="https://api.deepseek.com")
    
    # 清洗历史消息，只保留文本
    clean_history = []
    for msg in history:
        clean_history.append({"role": msg["role"], "content": str(msg["content"])})

    return client.chat.completions.create(
        model="deepseek-chat",
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
                                ph.markdown(clean_text(full_text) + "▌")
                        ph.markdown(clean_text(full_text))
                        st.session_state.history.append({"role": "assistant", "content": full_text})
                    except Exception as e:
                        st.error(f"讲解出错: {e}")
            else:
                status.update(label="识别失败", state="error")

# 显示历史对话
for msg in st.session_state.history:
    if msg["role"] != "system":
        # 如果是第一条题目内容，折叠显示
        if "题目内容如下" in str(msg["content"]) and msg["role"] == "user":
            with st.expander("查看识别到的题目"):
                st.markdown(clean_text(msg["content"]))
            continue
            
        with st.chat_message(msg["role"]):
            st.markdown(clean_text(msg["content"]))

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
                    ph.markdown(clean_text(full_text) + "▌")
            ph.markdown(clean_text(full_text))
            st.session_state.history.append({"role": "assistant", "content": full_text})
        except Exception as e:
            st.error(f"出错: {e}")
