import streamlit as st
import base64
from openai import OpenAI
from PIL import Image

def get_img_str(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

# 使用 cache_data 避免重复识别，节省 token 且优化体验
@st.cache_data(show_spinner=False)
def get_ocr_text(file_content):
    # 注意：st.cache_data 对 bytes 更友好，所以传入 content 而不是 UploadedFile 对象
    a = "sk-vogujjwsiclsbtlaorwvnncwfidlxavtukoxcqlciakmhtkr"
    b = "deepseek-ai/DeepSeek-OCR"
    
    # 建立连接
    client = OpenAI(
        api_key=a,
        base_url="https://api.siliconflow.cn/v1"
    )

    try:
        # d: 图片的 Base64 编码
        d = base64.b64encode(file_content).decode('utf-8')
        
        print(f"正在发送请求给模型: {b} ...")

        # e: 发送请求
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
        
        # 增强的后处理逻辑
        content = content.strip()
        
        # 1. 去除可能存在的 markdown 代码块包裹
        if content.startswith("```"):
            lines = content.split('\n')
            # 找到第一个换行符，通常第一行是 ```latex 或 ```json
            if len(lines) >= 2:
                # 重新组合，去掉第一行和最后一行
                content = "\n".join(lines[1:-1])
        
        # 2. 专门处理常见的 JSON 误判 (识别为 "}" 或 "{" ... "}")
        if content.endswith("}"):
            # 尝试查找对应的 "{"
            start_index = content.find("{")
            if start_index != -1:
                # 可能是 JSON，尝试提取 "content" 或 "text" 字段
                import json
                try:
                    json_data = json.loads(content[start_index:])
                    if isinstance(json_data, dict):
                        # 优先取 content, text, result 等字段
                        for key in ["content", "text", "result", "ocr_text"]:
                            if key in json_data:
                                content = json_data[key]
                                break
                except:
                    pass # 解析失败就当做普通文本
        
        return content

    except Exception as err:
        st.error(f"OCR出错: {err}")
        return None

def AI(messages):
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
            # 生成 markdown 内容
            md_content = f"# 错题记录 - {st.session_state.current_topic[:20]}...\n\n"
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

    # 功能 2：作文批改
    st.subheader("✍️ 作文批改")
    if st.button("📝 开启作文批改模式"):
        # 清空当前对话，切换系统提示词
        st.session_state.messages = [
            {"role": "system", "content": """
            你是一位资深的语文/英语作文批改老师。
            1. 请从【词汇运用】、【语法结构】、【逻辑连贯】、【内容深度】四个维度进行点评。
            2. 指出文中的亮点和不足。
            3. 给出修改建议和推荐的优美句式。
            4. 最后给出一个预估分数（满分100）。
            """}
        ]
        st.session_state.current_topic = "（作文批改模式）"
        st.session_state.messages.append({"role": "assistant", "content": "请直接发送你的作文内容（中文/英文均可），老师来帮你批改！"})
        st.rerun()

    st.divider()

    # 功能 3：英语口语陪练
    st.subheader("🗣️ 英语口语陪练")
    if st.button("🎙️ 开启口语对话"):
        st.session_state.messages = [
            {"role": "system", "content": """
            You are a friendly English tutor. 
            1. Converse with the student in simple, clear English.
            2. Correct their grammar mistakes gently in your reply.
            3. Keep the conversation going by asking open-ended questions.
            """}
        ]
        st.session_state.current_topic = "（英语口语模式）"
        st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm your English tutor. What topic would you like to talk about today?"})
        st.rerun()
    
    st.divider()

    # 功能 4：知识点百科
    st.subheader("📖 知识点百科")
    concept = st.text_input("输入想查询的概念（如：牛顿第二定律）")
    if st.button("🔍 查询讲解"):
        if concept:
            st.session_state.messages = [
                {"role": "system", "content": "你是一位博学的百科老师。请用通俗易懂的语言解释概念，并举出生活中的例子。"}
            ]
            st.session_state.current_topic = f"查询概念：{concept}"
            # 构造用户提问
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
/* 优化上传按钮样式 */
div[data-testid="stFileUploader"] label {
    font-size: 1.1rem !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

st.info("💡 提示：点击下方按钮，直接选择【拍照】或【相机】以上传题目。")

# 1. 只保留上传/系统相机模式
img_file = st.file_uploader(
    "📸 点击拍摄题目", 
    type=['jpg', 'png', 'jpeg'], 
    accept_multiple_files=False,
    key="uploader"
)

# 处理图片上传逻辑
if img_file:
    # 简单的文件ID生成，用于判断是否是新文件
    file_content = img_file.getvalue()
    file_id = f"{img_file.name}_{img_file.size}"
    
    # 如果是新上传的文件，进行 OCR 和初始化
    if file_id != st.session_state.last_uploaded_file_id:
        with st.spinner('正在识别题目...'):
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
                
                # 标记需要第一次回复
                st.session_state.need_first_response = True
                # 强制刷新以显示新状态
                st.rerun()

# 2. 显示识别到的题目（优化显示）
if st.session_state.current_topic:
    with st.expander("📝 查看识别到的题目", expanded=True):
        # 使用 markdown 渲染 LaTeX
        st.markdown(st.session_state.current_topic)

# 3. 聊天界面
st.subheader("👨‍🏫 老师讲解 & 答疑")

# 显示历史消息
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    if msg["role"] == "user" and "学生发来了这道题" in msg["content"]:
        continue 
        
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 处理首次自动回复 (流式)
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
    # 显示用户提问
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 显示 AI 回复
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
