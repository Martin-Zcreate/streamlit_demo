import streamlit as st
import base64
import io  # 新增：用于处理内存中的二进制流
from openai import OpenAI
from PIL import Image, ImageOps # 新增：用于图片压缩和旋转处理

# ================= 核心功能函数 =================

# 图片转 Base64 (本地文件用，目前主流程没用到，保留)
def get_img_str(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

# OCR 识别函数 (核心修改在这里)
@st.cache_data(show_spinner=False)
def get_ocr_text(file_content):
    # 你的 SiliconFlow API Key
    a = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr"
    b = "deepseek-ai/DeepSeek-OCR"
    
    client = OpenAI(
        api_key=a,
        base_url="https://api.siliconflow.cn/v1"
    )

    try:
        # ----------------- 图片预处理开始 -----------------
        # 1. 读取二进制数据为图片对象
        image = Image.open(io.BytesIO(file_content))
        
        # 2. 【关键】修复手机拍照的方向问题 (把横着的图扶正)
        image = ImageOps.exif_transpose(image)
        
        # 3. 限制最大尺寸 (防止 4000px 大图直接传，限制到 1024px 够用了)
        max_size = 1024
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size))
            
        # 4. 转为 RGB 模式 (防止 PNG 透明底导致报错)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        # 5. 压缩图片质量 (quality=60 能极大减小体积，防止 API 报错)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=60)
        
        # 6. 获取压缩后的 Base64
        d = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        print(f"原图: {len(file_content)/1024:.1f}KB -> 压缩后: {len(buffer.getvalue())/1024:.1f}KB")
        # ----------------- 图片预处理结束 -----------------

        print(f"正在发送请求给模型: {b} ...")

        # 发送请求
        e = client.chat.completions.create(
            model=b,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请提取图片中的文字和数学公式。重要要求：\n1. 所有数学公式（包括简单的变量如x, y）必须包含在 $ 符号中（行内公式）或 $$ 符号中（独立公式）。\n2. 不要输出任何 JSON 格式或 Markdown 代码块（如 ```json）。\n3. 只返回纯文本内容。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{d}"}}
                    ]
                }
            ],
            temperature=0.1,
        )

        content = e.choices[0].message.content
        content = content.strip()
        
        # 后处理：去除 Markdown 代码块包裹
        if content.startswith("```"):
            lines = content.split('\n')
            if len(lines) >= 2:
                content = "\n".join(lines[1:-1])
        
        # 后处理：防止 JSON 格式泄露
        if content.endswith("}"):
            start_index = content.find("{")
            if start_index != -1:
                import json
                try:
                    json_data = json.loads(content[start_index:])
                    if isinstance(json_data, dict):
                        for key in ["content", "text", "result", "ocr_text"]:
                            if key in json_data:
                                content = json_data[key]
                                break
                except:
                    pass 
        
        return content

    except Exception as err:
        st.error(f"OCR出错: {err}")
        return None

# AI 对话函数 (DeepSeek Chat)
def AI(messages):
    # 你的 DeepSeek 官方 API Key
    client = OpenAI(api_key="sk-af6ba48dbd8a4d1fb0d036551b9bbdc3",
                    base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )
    return response

# ================= 网页界面布局 =================

st.set_page_config(page_title="智酷AI作业帮手", page_icon="🤖", layout="wide")

# ================= 侧边栏：功能区 =================
with st.sidebar:
    st.title("🛠️ 实用工具箱")
    
    st.divider()
    
    # 功能 1：错题本导出
    st.subheader("📚 错题本")
    if st.button("📥 导出当前对话为 Markdown"):
        if st.session_state.messages:
            md_content = f"# 错题记录 - {str(st.session_state.current_topic)[:20]}...\n\n"
            md_content += f"## 📝 题目\n{st.session_state.current_topic}\n\n"
            md_content += "## 💡 讲解过程\n"
            for msg in st.session_state.messages:
                if msg["role"] == "assistant":
                    md_content += f"**老师**: {msg['content']}\n\n"
                elif msg["role"] == "user" and "学生发来了这道题" not in msg['content']:
                    md_content += f"**学生**: {msg['content']}\n\n"
            
            b64_md = base64.b64encode(md_content.encode()).decode()
            href = f'<a href="data:file/markdown;base64,{b64_md}" download="错题本.md">点击下载错题记录</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("暂无对话内容可导出")

    st.divider()

    # 功能 2：作文辅导
    st.subheader("✍️ 作文辅导")
    composition_title = st.text_input("输入作文题目（如：我的假期）")
    if st.button("📝 开始辅导"):
        if composition_title:
            st.session_state.messages = [
                {"role": "system", "content": """
                你是一位资深的作文辅导老师。
                1. 首先引导学生进行头脑风暴，列出写作大纲。
                2. 教授写作技巧（如：如何开头、如何描写细节）。
                3. 鼓励学生分段写作，并给出即时反馈。
                4. 最后给出一篇高质量的范文作为参考。
                """}
            ]
            st.session_state.current_topic = f"作文题目：{composition_title}"
            user_msg = f"老师，我要写一篇关于《{composition_title}》的作文，请教教我怎么写。"
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.need_first_response = True
            st.rerun()

    st.divider()

    # 功能 3：知识点百科
    st.subheader("📖 知识点百科")
    concept = st.text_input("输入想查询的概念（如：牛顿第二定律）")
    if st.button("🔍 查询讲解"):
        if concept:
            st.session_state.messages = [
                {"role": "system", "content": "你是一位博学的百科老师。请用通俗易懂的语言解释概念，并举出生活中的例子。"}
            ]
            st.session_state.current_topic = f"查询概念：{concept}"
            user_msg = f"请详细讲解一下【{concept}】这个知识点。"
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.need_first_response = True
            st.rerun()

# ================= 主界面 =================
st.title("🤖智酷AI作业帮手")

# 初始化 Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "last_uploaded_file_id" not in st.session_state:
    st.session_state.last_uploaded_file_id = None
if "need_first_response" not in st.session_state:
    st.session_state.need_first_response = False

st.markdown("""
<style>
div[data-testid="stFileUploader"] label {
    font-size: 1.1rem !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# 1. 上传/拍摄模块
img_file = st.file_uploader(
    "📸 点击拍摄题目 (或在左侧选择其他功能)", 
    type=['jpg', 'png', 'jpeg'], 
    accept_multiple_files=False,
    key="uploader"
)

# 处理图片上传逻辑
if img_file:
    file_content = img_file.getvalue()
    file_id = f"{img_file.name}_{img_file.size}"
    
    if file_id != st.session_state.last_uploaded_file_id:
        with st.spinner('正在处理图片并识别题目...'):
            # 调用带压缩功能的 OCR 函数
            ocr_result = get_ocr_text(file_content)
            
            if ocr_result:
                st.session_state.current_topic = ocr_result
                st.session_state.last_uploaded_file_id = file_id
                
                # 初始化新的对话
                st.session_state.messages = [
                    {"role": "system", "content": """
                    你是一位专业的老师。
                    1. 当学生问问题时，不要直接给完整答案。
                    2. 请使用"难度降级"法，把复杂的题目拆解成简单的步骤。
                    3. 先解释思路，再让学生去思考问题。
                    4. 公式请使用 LaTeX 格式，行内公式用 $ 包裹，独立公式用 $$ 包裹。
                    """},
                    {"role": "user", "content": f"学生发来了这道题，请讲解：\n{ocr_result}"}
                ]
                
                st.session_state.need_first_response = True
                st.rerun()

# 2. 显示识别到的题目
if st.session_state.current_topic:
    with st.expander("📝 查看识别到的题目", expanded=True):
        st.markdown(st.session_state.current_topic)

# 3. 聊天界面
st.subheader("👨‍🏫 老师讲解 & 答疑")

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    if msg["role"] == "user" and "学生发来了这道题" in msg["content"]:
        continue 
        
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 处理首次自动回复
if st.session_state.need_first_response:
    st.session_state.need_first_response = False
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        stream = AI(st.session_state.messages)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# 底部输入框
if prompt := st.chat_input("哪里不懂？可以继续问老师..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        stream = AI(st.session_state.messages)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
