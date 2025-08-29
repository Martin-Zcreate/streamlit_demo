from openai import OpenAI
import streamlit as st


def ai(p,ids):
    client = OpenAI(api_key="sk-db103a5ec442442bb66cc1b2e3187bf8", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": ids},
            {"role": "user", "content": p},
        ],
        stream=True
    )
    r=''
    ai_chat=st.chat_message("AI")
    ai_empty=ai_chat.empty()
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r


st.set_page_config(page_title="王欣文的AI助手🤣",
                   layout="wide",page_icon="🤣"
                   )
st.title("王欣文的AI助手🤣")

with st.sidebar:
    s = st.selectbox("选择ai的身份",
                     ("英语老师","数学老师","鲁迅","李白","周杰伦","王者荣耀官方"))
    if s=="英语老师":
        ids = """
         你是一名专业的英语老师,
         擅长教授初中生进行英语日常对话.
         在对话过程在判断用户是否标准,
         标准的话进行鼓励进一步的英语沟通,
         不标准的话进行纠正,
         引导用户进行英语对话.
         """
    elif s=="数学老师":
        ids = "你是一个专业的数学老师,教我二元一次方程"
    elif s=="鲁迅":
        ids = """你的身份是鲁迅,
        模仿鲁迅写的书的说话方式与用户对话,
        教授人生大道理
        """
    elif s=="李白":
        ids = """
        你的身份是李白,
        模仿李白写的诗的说话方式与用户对话.
        """
    elif s=="周杰伦":
        ids = """
        你的身份是周杰伦,
        教我唱周杰伦的歌.
        """
    elif s=="王者荣耀官方":
        ids = """
        你的身份是王者荣耀官方,
        教我如何上荣耀王者.
        """
a=st.chat_input("输入问题")

if "h" not in st.session_state:
    st.session_state["h"]=""
if "p" not in st.session_state:
    st.session_state["p"]=[]
    ai("你好",ids)
    
c=st.session_state["p"]
for i in c:
    st.chat_message("user").write(i[0])
    st.chat_message("AI").write(i[1])
    
if a is not None:
    st.chat_message("user").write(str(a))
    b = st.session_state["h"] + "用户:"+str(a)
    r = ai(b,ids)
    st.session_state["h"]+="用户:"+a+"\n"+"AI:"+str(r)+"\n"
    st.session_state["p"]+=[[a,str(r)]]
    
    
    
    


