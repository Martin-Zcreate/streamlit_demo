from openai import OpenAI
import streamlit as st


    
    
def ai(p,ids):
    client = OpenAI(api_key="sk-db103a5ec442442bb66cc1b2e3187bf8", base_url="https://api.deepseek.com")    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content":ids},
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


st.set_page_config(page_title="刘庭宇的AI助手🤣",
                   layout="wide",page_icon="🤣"
                   )

st.title("刘庭宇的AI助手🤣")



with st.sidebar:
    s=st.selectbox("选择AI身份",
                   ("英语老师","数学老师","鲁迅","音乐老师","李白","毛泽东"))
    if s=="英语老师":
        ids="""
        你是一个专业的英语老师,
        擅长教授初中生进行英语日常对话,
        在对话过程中判断用户说的是否标准,
        引导用户进行英语对话.
        """
    elif s=="数学老师":
        ids="你是一个初中数学老师,教我二元一次方程"
    elif s=="鲁迅":
        ids="模仿鲁迅的说话方式聊天"
    elif s=="音乐老师":
        ids="你是一个音乐老师,教我唱流行音乐"
    elif s=="李白":
        ids="你是大诗人李白,和我说话聊天"
    elif s=="毛泽东":
        ids="你是新中国主席毛泽东,向我询问新中国的现状"
        
        

if "h" not in st.session_state:
    st.session_state["h"]=""
if "p" not in st.session_state:
    st.session_state["p"]=[]
    ai("你好",ids)  
  
a=st.chat_input("输入问题")

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
    
    
    
    

