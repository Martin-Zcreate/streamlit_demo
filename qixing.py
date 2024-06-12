import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import requests
from io import StringIO
import base64
import json
from urllib.parse import quote


st.set_page_config(page_title="万载骑行数据统计AI", layout="wide", page_icon="🤖")
st.title("万载骑行数据统计AI")

def ai(prompt):
    r=''
    client = OpenAI(api_key="sk-fb2b9c1cc9934d1890b659d7a147f18d", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是 一个助手"},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    ai_chat=st.chat_message("AI")
    ai_empty=ai_chat.empty()
    for i in response:
        r+=i.choices[0].delta.content
        ai_empty.write(r)
    return r

def write(a,b,c):
    token = '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'

    owner = 'Martin-Zcreate'
    repo = 'streamlit_demo'
    file_path = c

    path_to_file = quote(file_path, safe='')

    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path_to_file}'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3.raw'
    }

    def get_sha():
        token = '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'
        owner = 'Martin-Zcreate'
        repo = 'streamlit_demo'
        path_to_file = quote(c, safe='')
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path_to_file}'
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_content = response.json()
            file_sha = file_content['sha']
            return file_sha


    file_sha = get_sha()

    # 发送GET请求以获取文件内容
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 文件内容是base64编码的，需要解码
        content = response.content
        decoded_content = content.decode('utf-8')
        # 使用StringIO将解码后的内容转换为文件对象
        data = StringIO(decoded_content)
        # 使用pandas读取CSV数据
        df = pd.read_csv(data)

        # 对DataFrame进行修改
        # 例如，添加一行
        
        if a==1:
            for i in range(len(b)-1):
                
                list3 = b[i].split(",")
                l1 =  list3[0]
                l2 =  list3[1]
                l3 =  list3[2]

                if df.index[df['会员号'] == int(l1)].all():
                    row_indices = df.index[df['会员号'] == int(l1)].tolist()
                    if row_indices != []:
                        df.loc[row_indices[0], l3] += 1
                else:
                    new_row = pd.Series({'会员号': int(l1), '名字': l2, l3: 1})
                    df = df.append(new_row, ignore_index=True)
                    
        else:
            new_df=pd.DataFrame(b,columns=['时间','发帖人', '会员参与人数','非会员人数', '骑行地点', '备注'])
            df = pd.concat([df, new_df], ignore_index=True)
        
        # 将修改后的DataFrame保存为CSV格式的字符串
        csv_string = df.to_csv(index=False)
        
        # 将CSV字符串编码为base64
        base64_csv = base64.b64encode(csv_string.encode('utf-8'))
        
        # 构建PUT请求的数据
        put_data = {
            'message': 'Update CSV file',
            'content': base64_csv.decode('utf-8'),
            'sha': file_sha  # 使用之前获取的文件SHA值
        }
        
        # 发送PUT请求以更新文件内容
        put_response = requests.put(url, headers=headers, data=json.dumps(put_data))
        
        # 检查响应状态码
        if put_response.status_code == 200:
            st.write(df)


def read(csv1):
    token = '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'
    owner = 'Martin-Zcreate'
    repo = 'streamlit_demo'
    path = csv1
    url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    request_url = url.format(owner=owner, repo=repo, path=path)
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    response = requests.get(request_url, headers=headers)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 文件内容是base64编码的，需要解码
        content = response.content
        decoded_content = content.decode('utf-8')
        # 使用StringIO将解码后的内容转换为文件对象
        data = StringIO(decoded_content)
        # 使用pandas读取CSV数据
        df = pd.read_csv(data)
        st.write(df)

if "df" not in st.session_state:
    st.session_state["df"]=read("聊天记录/data1.csv")
if "df2" not in st.session_state:
    st.session_state["df2"]=read("聊天记录/data2.csv")
    

st.session_state["list3"]=[]

prompt=st.chat_input("输入发帖信息")
if prompt is not None:
    s1 = """
    请把一下文字统计出跟帖人员数据形成以下格式,只要以下格式,不要其他文字。
    6个字段分别为时间(时间格式为x月x日x点x分)、发帖人(跟帖的第一个人)、
    会员参与人数(名字前面为序号,名字后面的数字为会员号,有会员号的为会员、没有的不是会员)、
    非会员人数、骑行地点、备注(填写非会员的名字)。
    格式为:
    '6月11日15点00分','49决策',9,3,'白良村部','踏浪、笨牛、芋头'
    """
    
    s2 = """
    请把一下文字统计出跟帖人员数据形成以下格式,只要以下格式,不要其他文字。
    会员定义:名字前面为序号,名字后面的数字为会员号,有会员号的为会员、没有的不是会员
    只统计会员,不是会员不统计,会员号放名字前面,如果会员号或名字相同,只保留一个(后面的),统计完一个会员要打句号:.
    会员号,名字,日期(日).
    例子:
    49,决策,11.
    
    """

    p1 = s1 + prompt
    p2 = s2 + prompt
    st.chat_message("user").write(prompt)
    
    r1=ai(p1)
    list1 = [r1.split(",")]
    r2 = ai(p2).split(".")
    
    write(0, list1, "聊天记录/data1.csv")
    write(1, r2, "聊天记录/data2.csv")
