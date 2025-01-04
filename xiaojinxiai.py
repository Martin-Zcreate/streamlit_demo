import streamlit as st
from openai import OpenAI

def ai(prompt):
    r = ''
    client = OpenAI(api_key="sk-bf8718c8164f50ad0861059db1aff7", base_url="https://api.deepseek.com/")
        
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """
             你的名字叫"小明",你可以帮助我学习.你是由万载第三中学七年级一班的肖晋汐开发的AI学习助手.
             """},
            {"role": "user", "content": prompt},
        ],
        stream=True 
    )
    ai_chat = st.chat_message("AI")
    ai_empty = ai_chat.empty()
    
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r
  
st.set_page_config(page_title="肖晋汐的AI学习助手",layout="wide",page_icon="👧")
st.title("肖晋汐的AI学习助手👧")

if "prompt" not in st.session_state:
    st.session_state["prompt"]=[]
if "history" not in st.session_state:
        st.session_state["history"]=''
        ai("介绍你自己")

prompt = st.chat_input("请输入问题")
with st.sidebar:
    p1 = st.text_input("输入文字")
    if st.button("写语文作文"):
        prompt = f"写一篇500字以上的中学作文,题目为{p1},尽量用生活中的例子,真情实感,主人公是一个女生,万载第三中学初一的学生,他生活在江西省万载县的县城内"
    
    if st.button("做数学题目"):
        prompt = f"求以下数学题:{p1},像中小学数学老师给出解题思路/方法,并给出解题的过程和通俗易懂的讲解,给出计算过程和答案"
    
    if st.button("写语文作文开头和框架"):
        prompt = f"写中学作文标题为:{p1}的5个开头和思路框架,方便我获得灵感"
    
    if st.button("写英语作文"):
        prompt = f"写中学英语作文,题目为:{p1},60个单词以上,单词范围在初中以内,每一句英语后翻译为中文,并中学老师的口吻中文讲解这篇作文的写法"
    if st.button("背英语单词"):
        prompt="""
        请你帮我生成20个（测试单词个数）中国人教版初中（学习科目）常用英语词汇，一个一个的生成，
        每次生成的时候询问我是否认识单词（测试形式），如果我回答“yes”请给出这个单词的音标和生成下一个单词，
        如果我回答“no”（回答形式和判断条件），请给出这个单词的音标和中文释义，
        词性和使用例句和辅助背单词的形象解释（生成单词内容）再生成下一个单词。
        """
    
    if st.button("yes"):
        prompt="yes"
    if st.button("no"):
        prompt="no"
    
    
st.session_state["history"]=''
for i in range(len(st.session_state["prompt"])):
    st.chat_message("user").write(st.session_state["prompt"][i][0])
    st.chat_message("AI").write(st.session_state["prompt"][i][1])
    st.session_state["history"] += "user:" + st.session_state["prompt"][i][0] + "\n"
    st.session_state["history"] += "system:" + st.session_state["prompt"][i][1] + "\n"

if prompt is not None:
    st.session_state["history"] += prompt
    st.chat_message("user").write(prompt)
    
    r=ai(st.session_state["history"])
    st.session_state["prompt"] += [[prompt,r]]
    
