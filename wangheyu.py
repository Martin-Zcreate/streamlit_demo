import streamlit as st
import requests  
import json
import jieba

st.set_page_config(page_title="语文学习机", layout="centered", page_icon="☘")  
  
API_KEY = "dzAbTdjG6Tv7dg2R6V1fLgXL"  
SECRET_KEY = "24GdUqOz4FlhQpGGGPntxBmKN8obgktq" 

def p1():
    if "chat_history" not in st.session_state:  
        st.session_state["chat_history"] = []  
      
    def main(prompt):  
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()  
      
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
        st.title("王鹤宇的语文学习机🧑")
        user_input = st.chat_input("在这里输入问题")
    
        with st.sidebar:
            st.sidebar.title("王鹤宇的语文学习机🧑")
            if st.sidebar.button("背一首诗"):
                user_input = """
                我叫王鹤宇,请你以后这样叫我,是一名七年级的初中生,
                我想提高我的语文成绩,请你提供一首七年级人教版语文课本的
                诗,我来进行背诵,并讲解它的背景与译文
                
                """
        
        if st.sidebar.button("名著重点知识"):
            user_input = """
            我叫王鹤宇,请你以后这样叫我,是一名七年级的初中生,
            我想提高我的语文成绩,请你提供七年级的一本名著中的
            重点知识
            """
    
        if st.sidebar.button("语文阅读题的答题技巧"):
            user_input = """
            我叫王鹤宇,请你以后这样叫我,是一名七年级的初中生,
            我想提高我的语文成绩,请你列出做阅读题通常会问的
            问题与它的答题框架与技巧
            """
    
        if st.sidebar.button("语文优美词汇积累"):
            user_input = """
            我叫王鹤宇,请你以后这样叫我,是一名七年级的初中生,
            我想提高我的语文成绩,请你写20个语文中的优美词汇,
            不重复,要有2个字的与4个字的词汇,在词汇后面写上
            拼音并写上意思
            """
            
        if user_input is not None:
            progress_bar = st.empty()
            
            with st.spinner("内容已提交,作者正在苦思"):
                feedback = json.loads(main(user_input))["result"]
                if feedback:
                    progress_bar.progress(100)
                    st.session_state['chat_history'].append((user_input,feedback))
                    
                    for i in range(len(st.session_state['chat_history'])):
                        user_info = st.chat_message("user")
                        user_content = st.session_state['chat_history'][i][0]
                        user_info.write(user_content)
                        
                        AI_info = st.chat_message("assistant")
                        AI_content = st.session_state['chat_history'][i][1]
                        AI_info.write(AI_content)
                    
                else:
                    st.info("对不起,回答不了,请换一个问题吧🤡")

def p2():
    st.title("文章词汇分析")
    txt = st.text_area(
    "输入文字",
    """
    
    """
    )
    if st.button("确认提交"):
        st.write(f'你写了{len(txt)}个字')
        list1 = jieba.lcut(txt)
        
        counts = {}
        for i in list1:
            if len(i) == 1:
                continue
            counts[i] = counts.get(i,0)+1
        
        list4 = list(counts.items())
        list4.sort(key=lambda x: x[1],reverse=1)
        list5 = list4[0:100]
        d1 = dict(list5)
        
        list2 = list(d1.keys())
        list3 = list(d1.values())
        from pyecharts import options as opts
        from pyecharts.charts import Bar
        from pyecharts.faker import Faker
        from streamlit_echarts import st_pyecharts
        
        c = (
            Bar()
            .add_xaxis(list2)
            .add_yaxis(" ",list3, color="blue"and"red")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="词频统计"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            )
        )
        st_pyecharts(c)
        
    
pagef = {
    "王鹤宇的主页":p1,
    "统计词汇":p2
    }

s = st.sidebar.selectbox("选择页面",pagef.keys())
pagef[s]()
