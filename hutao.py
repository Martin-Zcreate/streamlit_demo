import streamlit as st
import requests  
import json
st.set_page_config(page_title="桃门专属AI", layout="centered", page_icon="🤖")  
  
API_KEY = "ZB7qXhepNoq0B9HCGGvr6v8Z"  
SECRET_KEY = "p52DihWmG17m9jf1xjNw7n0gbjTzwBGa" 

def intro():
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
        st.title("一个胡桃厨的专属AI")
        user_input = st.chat_input("加入桃门,在这里输入问题")
        
        
        with st.sidebar:
            st.sidebar.title("一个胡桃厨的专属AI")
        if user_input is not None:
            progress_bar = st.empty()
            with st.spinner("内容已提交,且听我传教:加入桃门吧"):
                feedback = json.loads(main(user_input))["result"]
                if feedback:
                    progress_bar.progress(100)
                    st.session_state['chat_history'].append((user_input,feedback))
                    for i in range(len(st.session_state['chat_history'])):
                        user_info =st.chat_message("user")
                        user_content = st.session_state['chat_history'][i][0]
                        user_info.write(user_content)
                        
                        AI_info =st.chat_message("asslistant")
                        AI_content = st.session_state['chat_history'][i][1]
                        AI_info.write(AI_content)
                        
                else:
                    st.info("对不起,无法回答,许是往生堂没业绩哦,请送业绩来")
intro()
                    
                
                
                
                
