import streamlit as st
import base64
import re
import io
from PIL import Image, ImageOps
from openai import OpenAI

# ================= 配置区域 =================
# ⚠️ 请填入你的硅基流动 API Key
# 注册地址: https://cloud.siliconflow.cn/
API_KEY = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr" 

# 模型配置
OCR_MODEL = "deepseek-ai/DeepSeek-OCR"
CHAT_MODEL = "deepseek-ai/DeepSeek-V3" # 或者 deepseek-ai/DeepSeek-R1

# ================= 工具函数 =================

def clean_latex(text):
    """
    清洗 LaTeX 格式以便 Streamlit 正确渲染
    """
    if not text:
        return ""
    # 替换块级公式 \[ ... \] -> $$ ... $$
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    # 替换行内公式 \( ... \) -> $ ... $
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
    # 移除 Markdown 代码块标记，防止公式被包裹在代码块里不渲染
    text = re.sub(r'```latex', '', text)
    text = re.sub(r'```', '', text)
    return text

def process_image(image_bytes, max_mb=4):
    """
    图片预处理终极版：
    1. 修正 EXIF 旋转 (手机拍照必做)
    2. 修复 PNG 透明背景变黑 (转白底)
    3. 智能压缩：仅当图片 > 4MB 时才压缩，最大程度保留细节
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # 1. 修正旋转 (手机竖拍照片常带旋转角)
        img = ImageOps.exif_transpose(img)
        
        # 2. 处理颜色模式 (RGBA转RGB，透明变白)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            bg.paste(img, mask=img.split()[-1]) # 使用 alpha 通道做掩码
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 3. 检查大小
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95) # 默认高质量
        size_bytes = len(buf.getvalue())
        limit_bytes = max_mb * 1024 * 1024
        
        # 如果小于限制，直接返回
        if size_bytes <= limit_bytes:
            return buf.getvalue()

        # 4. 超出限制则循环压缩
        quality = 90
        scale = 0.9
        w, h = img.size
        
        while size_bytes > limit_bytes:
            buf = io.BytesIO()
            nw, nh = int(w * scale), int(h * scale)
            resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
            resized.save(buf, format="JPEG", quality=quality)
            
            size_bytes = len(buf.getvalue())
            
            scale *= 0.8
            if scale < 0.3: break 
            
        return buf.getvalue()

    except Exception as e:
        st.error(f"图片处理异常: {e}")
        return image_bytes

def get_ocr_text(image_bytes):
    """
    调用 OCR，参数严格对齐 Playground 截图
    """
    client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")

    try:
        b64_img = base64.b64encode(image_bytes).decode('utf-8')
        
        response = client.chat.completions.create(
            model=OCR_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请提取图中所有内容，数学公式请务必使用 LaTeX 格式（行内用 $，独占行用 $$）。不要包含原本没有的解释文字。"},
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_img}",
                                "detail": "high" # ⚡️关键：强制高清模式
                            }
                        }
                    ]
                }
            ],
            # === 根据截图调整的参数 ===
            temperature=0.0,       # 截图设置：0.0
            top_p=0.7,             # 截图设置：0.7
            max_tokens=4096,       # 截图设置：4096
            frequency_penalty=0.0  # 截图设置：0.0
            # ========================
        )
        
        return clean_latex(response.choices[0].message.content)

    except Exception as e:
        st.error(f"OCR 请求失败: {e}")
        return None

def ai_stream(messages):
    """
    调用对话模型 (DeepSeek-V3/R1)
    """
    client = OpenAI(api_key=API_KEY, base_url="https://api.siliconflow.cn/v1")
    
    # 清理消息历史，确保只发送文本给对话模型（避免格式错误）
    text_msgs = []
    for m in messages:
        # 只取文本内容
        text_msgs.append({"role": m["role"], "content": m["content"]})

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=text_msgs,
        stream=True,
        temperature=0.7 # 讲题可以稍微灵活一点
    )
    return response

# ================= 页面主逻辑 =================

st.set_page_config(page_title="AI 题目讲解", page_icon="🎓")
st.title("🎓 AI 题目讲解助手")
st.caption("基于 DeepSeek-OCR & DeepSeek-V3 | 硅基流动强力驱动")

# 状态初始化
if "history" not in st.session_state:
    st.session_state.history = []
if "last_file" not in st.session_state:
    st.session_state.last_file = None
if "ocr_content" not in st.session_state:
    st.session_state.ocr_content = None

# 系统提示词
SYSTEM_PROMPT = """
你是一位耐心、专业的老师。
1. 拿到题目内容后，先梳理思路，再逐步讲解。
2. 遇到数学公式，必须使用 LaTeX 格式：行内用 $...$，独立公式用 $$...$$。
3. 讲解要清晰易懂，适合学生阅读。
"""

# 上传组件
uploaded_file = st.file_uploader("📸 拍照或上传图片", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    file_id = f"{uploaded_file.name}-{uploaded_file.size}"
    
    # 发现新图片，开始处理
    if st.session_state.last_file != file_id:
        st.session_state.last_file = file_id
        st.session_state.history = [] # 清空旧聊天
        st.session_state.ocr_content = None
        
        raw_bytes = uploaded_file.getvalue()
        
        with st.status("🔍 正在分析图片...", expanded=True) as status:
            st.write("🛠️ 图片预处理 (旋转修正/去噪/尺寸优化)...")
            processed_bytes = process_image(raw_bytes)
            
            st.write("🚀 正在识别文字与公式 (DeepSeek-OCR)...")
            ocr_text = get_ocr_text(processed_bytes)
            
            if ocr_text:
                st.session_state.ocr_content = ocr_text
                status.update(label="识别成功", state="complete", expanded=False)
                
                # 构造初始对话
                init_msg = f"这是识别到的题目内容：\n\n{ocr_text}\n\n请老师帮我讲解这道题。"
                # 存入 system prompt 和 第一条 user msg
                st.session_state.history = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": init_msg}
                ]
                
                # === 自动触发第一次讲解 ===
                with st.chat_message("assistant"):
                    ph = st.empty()
                    full_res = ""
                    try:
                        stream = ai_stream(st.session_state.history)
                        for chunk in stream:
                            txt = chunk.choices[0].delta.content
                            if txt:
                                full_res += txt
                                ph.markdown(clean_latex(full_res) + "▌")
                        ph.markdown(clean_latex(full_res))
                        st.session_state.history.append({"role": "assistant", "content": full_res})
                    except Exception as e:
                        st.error(f"生成讲解出错: {e}")
            else:
                status.update(label="识别失败", state="error")
                st.error("无法提取内容，请检查图片是否清晰。")

# === 界面显示 ===

# 1. 显示识别的原文 (可折叠)
if st.session_state.ocr_content:
    with st.expander("查看原始 OCR 识别结果", expanded=False):
        st.markdown(st.session_state.ocr_content)

# 2. 聊天区域
st.divider()

# 渲染历史记录 (跳过 system 和 第一条 user 消息，避免重复显示题目)
for i, msg in enumerate(st.session_state.history):
    if msg["role"] == "system": continue
    # 如果想把第一条包含题目内容的 user 消息隐藏，可以取消下面这行的注释
    # if i == 1: continue 
    
    with st.chat_message(msg["role"]):
        st.markdown(clean_latex(msg["content"]))

# 3. 追问输入框
if prompt := st.chat_input("还有哪里不懂？"):
    # 显示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})
    
    # AI 回复
    with st.chat_message("assistant"):
        ph = st.empty()
        full_res = ""
        try:
            stream = ai_stream(st.session_state.history)
            for chunk in stream:
                txt = chunk.choices[0].delta.content
                if txt:
                    full_res += txt
                    ph.markdown(clean_latex(full_res) + "▌")
            ph.markdown(clean_latex(full_res))
            st.session_state.history.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"回复出错: {e}")
