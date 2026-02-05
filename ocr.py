import streamlit as st
import base64
import re
import io
from PIL import Image, ImageOps  # 必须引入 ImageOps 处理手机照片旋转
from openai import OpenAI

# ================= 配置区域 =================
OCR_KEY = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr" 
CHAT_KEY = "sk-af6ba48dbd8a4d1fb0d036551b9bbdc3"
# ===========================================

def clean_latex(text):
    """
    清洗 LaTeX 格式以便 Streamlit 渲染
    """
    if not text:
        return text
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.DOTALL)
    return text

def compress_image(image_bytes, max_size_kb=1024): # 改大到 1MB
    """
    处理图片：修正旋转、保持彩色、适度压缩
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # 1. 修正手机拍照的旋转信息 (关键)
        img = ImageOps.exif_transpose(img)
        
        # 2. 强制转为 RGB，防止灰度图导致 OCR 识别率下降 (关键)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 准备输出
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        d = buf.getvalue() # d = data

        # 如果本身就小于限制，直接返回
        if len(d) <= max_size_kb * 1024:
            return d

        # 3. 循环压缩逻辑
        q = 90 # quality
        w, h = img.size
        s = 1.0 # scale
        
        while True:
            buf = io.BytesIO()
            if s < 1.0:
                # 缩放尺寸
                nw = int(w * s)
                nh = int(h * s)
                # 使用 LANCZOS 算法保持文字边缘清晰
                img_r = img.resize((nw, nh), Image.Resampling.LANCZOS)
                img_r.save(buf, format="JPEG", quality=q)
            else:
                img.save(buf, format="JPEG", quality=q)
            
            d = buf.getvalue()
            
            if len(d) <= max_size_kb * 1024:
                return d
            
            # 调整参数
            if q > 70:
                q -= 10
            else:
                s *= 0.8
                
            if s < 0.2: # 防止缩太小完全看不清
                return d

    except Exception as e:
        st.warning(f"处理图片出错: {e}")
        return image_bytes

def get_ocr_text(image_bytes):
    # 使用配置好的 Key
    client = OpenAI(
        api_key=OCR_KEY, 
        base_url="https://api.siliconflow.cn/v1"
    )

    try:
        d = base64.b64encode(image_bytes).decode('utf-8')
        
        resp = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-OCR",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请提取图中所有文字和公式。行内公式用 $...$，独立公式用 $$...$$。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{d}"}}
                    ]
                }
            ],
            temperature=0.1,
        )

        content = resp.choices[0].message.content
        return clean_latex(content)

    except Exception as err:
        st.error(f"OCR请求失败: {err}")
        return None

def AI_stream(messages):
    client = OpenAI(
        api_key=CHAT_KEY,
        base_url="https://api.deepseek.com"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )
    return response

# ================= 网页界面布局 =================

st.title("🤖 AI 作业帮手")
st.write("用手机拍下题目，AI 帮你拆解思路。")

# 初始化状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_id" not in st.session_state:
    st.session_state.last_id = None
if "ocr_res" not in st.session_state:
    st.session_state.ocr_res = None

SYSTEM_PROMPT = """
你是一位专业的老师。
1. 难度降级：把复杂题目拆解成简单步骤。
2. 引导思考：不要直接给代码，先讲思路。
3. 格式规范：公式使用 LaTeX，行内用 $，独立用 $$。
"""

img_file = st.file_uploader(
    "📸 点击拍摄题目", 
    type=['jpg', 'png', 'jpeg'], 
    key="uploader"
)

if img_file:
    fid = f"{img_file.name}-{img_file.size}"
    
    # 新文件处理
    if st.session_state.last_id != fid:
        st.session_state.last_id = fid
        st.session_state.messages = []
        st.session_state.ocr_res = None
        
        raw_bytes = img_file.getvalue()
        
        # 显示处理状态
        with st.status("正在处理图片...", expanded=True) as status:
            st.write("🔄 正在修正方向与优化体积...")
            # 压缩处理
            proc_bytes = compress_image(raw_bytes, max_size_kb=1024)
            
            st.write("🔍 正在识别题目内容...")
            # OCR 识别
            st.session_state.ocr_res = get_ocr_text(proc_bytes)
            status.update(label="处理完成", state="complete", expanded=False)

    # 结果展示与对话
    if st.session_state.ocr_res:
        txt = st.session_state.ocr_res
        
        st.subheader("📝 识别结果")
        st.markdown(txt)
        
        st.subheader("👨‍🏫 老师讲解")
        
        # 首次自动触发讲解
        if not st.session_state.messages:
            u_msg = f"题目内容：\n{txt}\n\n请讲解这道题。"
            st.session_state.messages.append({"role": "user", "content": u_msg})
            
            api_msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            
            with st.chat_message("assistant"):
                ph = st.empty()
                full_res = ""
                try:
                    stream = AI_stream(api_msgs)
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_res += chunk.choices[0].delta.content
                            ph.markdown(clean_latex(full_res))
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"AI 响应出错: {e}")

        # 渲染历史消息 (跳过第一条隐含的 User 消息)
        else:
            for i, msg in enumerate(st.session_state.messages):
                if i == 0 and msg["role"] == "user":
                    continue
                with st.chat_message(msg["role"]):
                    st.markdown(clean_latex(msg["content"]))

        # 底部输入框
        if prompt := st.chat_input("哪里不懂？继续问..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                ph = st.empty()
                full_res = ""
                api_msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                
                try:
                    stream = AI_stream(api_msgs)
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_res += chunk.choices[0].delta.content
                            ph.markdown(clean_latex(full_res))
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"AI 响应出错: {e}")
