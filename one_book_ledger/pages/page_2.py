import streamlit as st

st.set_page_config(page_title="Page 2", page_icon="📊") # 设置页面配置 (可选)

# st.sidebar.header("Page 2 侧边栏") # 为当前页面添加侧边栏内容

st.title("这是 Page 2")

st.line_chart({"data": [1, 5, 2, 6, 2, 1]}) # Page 2 特有的组件