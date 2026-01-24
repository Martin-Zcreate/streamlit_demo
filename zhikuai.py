import streamlit as st
import random
import time

st.set_page_config(layout="wide", page_title="AI 通信实验室")

# 字典：摩尔斯码
d = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.',
      'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..',
      'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.',
      'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
      'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--',
      '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
      '9':'----.', '0':'-----', ',':'--..--', '.':'.-.-.-', '?':'..--..',
      '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-' }

# 1. 初始化状态：如果内存里没存这两个变量，就先赋默认值
if 's1' not in st.session_state: st.session_state.s1 = "等待输入..."  # s1: 左侧显示内容
if 's2' not in st.session_state: st.session_state.s2 = "点击按钮接收总部指令..." # s2: 右侧显示内容

# 2. 样式：给按钮加默认灰色背景，防止隐身；再分别为两栏上色
st.markdown("""
<style>

    /* 标题颜色调整 */
    h3 { color: #4285F4 !important; font-weight: 700 !important; }
    /* 按钮通用：白字，圆角，默认灰色底(防隐身) */
    .stButton>button { color: white !important; border-radius: 8px; background-color: #999; border: none; width: 100%; }
    /* 左栏按钮(第1个)变橙色 */
    div[data-testid="column"]:nth-of-type(1) .stButton>button { background-color: #F46820; }
    /* 右栏按钮(第2个)变蓝色 */
    div[data-testid="column"]:nth-of-type(2) .stButton>button { background-color: #4285F4; }
    /* 黑盒子样式 */
    .box { background-color: #1F2430; color: #98C379; padding: 20px; border-radius: 8px; min-height: 150px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("## AI 通信实验室 <span style='color:#F46820;font-size:0.6em'>(Powered by zhiku)</span>", unsafe_allow_html=True)

# 布局：分两列
c1, c2 = st.columns(2)

# === 左侧逻辑 ===
with c1:
    with st.container(border=True):
        st.subheader("🔠 智能电报员")
        st.caption("输入话语，转为电报体和摩斯码。")
        t = st.text_area("输入:", height=100, placeholder="例如: SOS") # t: 输入文本
        
        # 按钮点击后，只更新内存(session_state)，不直接打印
        if st.button("⚡ 翻译并发送"):
            if t:
                # 查表翻译，没查到的变问号，用空格连接
                res = ' '.join([d.get(x, '?') for x in t.upper()]) # res: 临时结果
                st.session_state.s1 = f"发送中...\n\n{res}" # 更新 s1
            else:
                st.session_state.s1 = "请先输入内容！" 
        
        # 显示黑盒子（永远显示 s1 的内容）
        st.markdown(f'<div class="box">{st.session_state.s1}</div>', unsafe_allow_html=True)

# === 右侧逻辑 ===
with c2:
    with st.container(border=True):
        st.subheader("🕵️ 绝密任务生成器")
        st.caption("点击获取你的代号和任务。")
        st.write("") # 占位对齐
        st.write("") 
        
        # 任务库
        lst = [
            "代号：夜莺。任务：去楼下便利店买仅剩的一瓶快乐水。",
            "代号：黄昏。任务：假装在看风景，实则观察猫咪的动向。",
            "代号：007。任务：今晚不许熬夜，并在23:00前入睡。",
            "代号：幽灵。任务：给好久没联系的朋友发一个表情包。"
        ]
        
        # 按钮点击
        if st.button("🎲 获取绝密任务"):
            with st.spinner("指令接收中..."):
                time.sleep(0.5)
                # 随机抽一个存入 s2
                st.session_state.s2 = f">>> 接收成功\n\n{random.choice(lst)}"
        
        # 显示黑盒子（永远显示 s2 的内容）
        st.markdown(f'<div class="box">{st.session_state.s2}</div>', unsafe_allow_html=True)
