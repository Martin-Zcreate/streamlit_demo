import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from streamlit_echarts import st_pyecharts
import requests
import json

API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 
st.set_page_config(page_title="学科数据分析", layout="centered", page_icon="💡") 

def p1():
    st.title("欢迎来到📈学科数据分析📉(¬‿¬)")
    st.markdown("作者:戴震铭")
    st.header("不看一天难受,看了难受一天🤡")
    st.write("""擦亮眼睛看看自己的实力!!!!
              """)
    
def p2():
    st.header("本网站做的十分炸裂")
    st.write("""
              如有不满请轰炸\n
              如十分满意请不必隐晦褒奖之词\n
              Q:656552723""")

def p3():
    st.title("由于业务繁忙,作者无法立即更新")
    st.header("公元2024年二月九日零点停服更新")
    st.write("敬请期待.......")
              
def pie():
    st.title("📈学科数据分析📉")
    name = st.text_input("请输入你的姓名")
    v = ["语文📕","数学📐","英语🎄","物理🗜","化学🧪","生物🧬","地理🌏","历史🗿","政治📄"]
    predict_size = 1
                  
    cols = st.columns(len(v))
    lists = []
                    
    for p in range(len(v)):
        lists.append([])
                        
    for i, c in enumerate(cols):
        with c:
            for j in range(1):
                key = f"number_input_{i}_{j}"
                a = st.number_input(v[i], key=key)
                lists[i].append(a)
    
    
    df = pd.DataFrame(lists)
    df = df.transpose()
    df.columns = v
    st.write(df)
    
    
    # st.markdown(f"{lists}")
    
    
    lista = []
    for i in lists:
        if i[0] == 0:
            i = None
        else:
            i = i[0]
        lista += [i]
    
    if st.button("🧐开始分析"):
        k1 = []
       
        for i in zip(v,lista):
            k1 += i
        
        
        with st.columns(3)[1]:
         st.header(f"{name}的数据")
        c = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(v,lista)],
                radius=["30%", "80%"],
                center=["45%", "60%"],
                rosetype="area",
            )
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        st_pyecharts(c)
            
        
        if "chat_history" not in st.session_state:  
            st.session_state["chat_history"] = []  
          
        def main(prompt):  
            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()  
          
            payload = json.dumps({  
                "messages": [  
                    {  
                        "role": "user",  
                        "content": prompt  
                    }  
                ]  
            })  
            headers = {  
                'Content-Type': 'application/json'  
            }  
          
            response = requests.request("POST", url, headers=headers, data=payload)  
          
            return response.text
        
        def get_access_token():  
            """  
            使用 AK，SK 生成鉴权签名（Access Token）  
            :return: access_token，或是None(如果错误)  
            """  
            url = "https://aip.baidubce.com/oauth/2.0/token"  
            params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}  
            return str(requests.post(url, params=params).json().get("access_token"))
        
        if __name__ == '__main__':
            st.title("📈学科数据分析📉")
            
            
            with st.sidebar:
                if st.sidebar.button("清空对话历史"):
                    st.session_state["chat_history"] = []
                user_input =f"""
                    我叫{name},请你以后这样称呼我,
                    我是一个8年级的初生,
                    以下是我的学科成绩,
                    请你列举出我的优势科目以及劣势科目,
                    并分析一下我的成绩.
                    {k1}
                """
            
            
            if user_input is not None:
                progress_bar = st.empty()
                with st.spinner("内容已提交,正在冥想中!"):
                    feedback = json.loads(main(user_input))["result"]
                    if feedback:
                        progress_bar.progress(100)
                        st.session_state['chat_history'].append((user_input,feedback))
                        for i in range(len(st.session_state["chat_history"])):
                            user_info = st.chat_message("user")
                            user_content = st.session_state['chat_history'][i][0]
                            user_info.write(user_content)
                            
                            assistant_info = st.chat_message("assistant")
                            assistant_content = st.session_state['chat_history'][i][1]
                            assistant_info.write(assistant_content)
                            
                            
                                
                    else:
                        st.info("对不起,请重新输入🤡")
    
    
with st.sidebar:
    st.markdown("# 🐱‍🏍戴震铭的个人网页")
    
pagef = {
    "主页":p1,
    "数据分析" : pie,
    "历史记录":p3,
    "提出意见" : p2
    }

s = st.sidebar.selectbox(
    "选择页面",pagef.keys()
    )
pagef[s]()
    