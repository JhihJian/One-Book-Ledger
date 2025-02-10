import streamlit as st
import pandas as pd
import io
import chardet



st.title("CSV 文件阅读器")
uploaded_file = st.file_uploader("上传 CSV 文件", type="csv")
encoding_options = ['utf-8', 'gbk']
selected_encoding_name = st.selectbox("选择文件编码 (可选，自动检测默认)", encoding_options, index=0)

skip_rows_default = 0
skip_rows = st.number_input("跳过文件头行数 (可选，自动检测默认)", min_value=0, value=skip_rows_default, step=1)


if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read() # Read file content into bytes *once*

        # Create io.BytesIO object from bytes data for pd.read_csv
        file_like_object = io.BytesIO(file_bytes)

        df = pd.read_csv(
            file_like_object, # Use the in-memory file-like object
            skiprows=skip_rows,
            encoding=selected_encoding_name
        )

        if df is not None:
            st.dataframe(df.head(100))
        else:
            st.error("**读取 CSV 文件失败，请检查文件格式或尝试手动设置编码和跳过行数。** (详细错误信息请查看控制台)")

    except pd.errors.ParserError:
        st.error("**文件解析错误！**\n\n请确保上传的是 **标准的 CSV 文件**，并且文件内容符合 CSV 格式。\n\n**可能原因和解决方法:**\n* 文件可能不是标准的 CSV 格式，或者内容损坏。\n* 文件分隔符可能选择不正确，请尝试在 '选择分隔符' 中选择其他分隔符。\n* 如果程序未能正确自动检测跳过行数，请手动调整 **'跳过文件头行数'** 设置。\n* 文件编码格式可能不正确，请尝试在 **'选择文件编码'** 下拉菜单中尝试其他编码格式。")
    except Exception as e:
        st.error(f"Streamlit 应用发生未知错误：{e}")