from openai import OpenAI
import streamlit as st

def AI(p):
    client = OpenAI(api_key="sk-767336726c4045a9a228a02eb697dea3",
                    base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": 
             
             """
              你是辛子瑜的作文帮手,专门教六年级的语文作文,
              用户会给你一个作文题目和作文类型,
              你需要写一篇六年级学生水平的作文.水平差一些,写点错别字.
              字数要求600字.
              用户身份背景,万载一小,六年级三班.
              家住在万载,11岁,爸爸妈妈在家里一起生活
             """
             
             },
            {"role": "user", "content": p},
        ],
        stream=True
    )
    r=""
    ai_chat = st.chat_message("AI")
    ai_empty = ai_chat.empty()
    
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r 

st.title("智酷机器人的AI🚗")

if "p" not in st.session_state:
    st.session_state["p"] = []
if "h" not in st.session_state:
    st.session_state["h"] = ""
    AI("你是谁?")
    
p = st.chat_input("请输入问题🤣")

st.session_state["h"] = ""


for i in range(len(st.session_state["p"])):
    st.chat_message("user").write(st.session_state["p"][i][0])
    st.chat_message("AI").write(st.session_state["p"][i][1])
    
    st.session_state["h"] += "user:"+st.session_state["p"][i][0]+"\n"
    st.session_state["h"] += "system:"+st.session_state["p"][i][1]+"\n"
    
    


if p is not None:
    st.session_state["h"] += p
    st.chat_message("user").write(p)
    r = AI(st.session_state["h"])
    st.session_state["p"]+=[[p,r]]
