import streamlit as st
import pandas as pd
st.title('伍某某的成绩管理系统📃📜📄💵')
if st.button('开始/清空'):
    st.session_state['s']=[]
a1=st.text_input('输入姓名')
a2=st.number_input('输入语文成绩🏫')
a3=st.number_input('输入数学成绩🏫')
a4=st.number_input('输入英语成绩🏫') 
a5=a2+a3+a4 
a6=a5/3 
if st.button('提交'):
    st.session_state['s'].append([a1,a2,a3,a4,a5,a6])
    df=pd.DataFrame(st.session_state['s'],columns=['姓名','语文','数学','英语','总分','平均分'])
    st.dataframe(df,width=1000)
    st.bar_chart(df,x='姓名',y=['语文','数学','英语'])
