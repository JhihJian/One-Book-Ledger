import streamlit as st
from database_helper import DatabaseHelper
from upload_handler import bill_file_uploader

# 预定义的账单类型
BILL_TYPES = ["微信账单", "支付宝账单", "中信银行账单", "浦发银行账单"]

def main():
    st.title("One-Book-Ledger - 账单文件列表")
    st.header("账单文件管理")

    # Initialize session_state
    if "bill_files_data" not in st.session_state:
        st.session_state.bill_files_data = []
    if "bill_file_content" not in st.session_state:  # Initialize bill_file_content in session_state
        st.session_state.bill_file_content = None

    db_helper = DatabaseHelper()
    st.session_state.bill_files_data = db_helper.get_bill_files()
    db_helper.close_connection()

    if st.session_state.bill_files_data:
        st.subheader("已上传账单文件")
        #  使用 st.dataframe 展示数据
        st.dataframe(
            st.session_state.bill_files_data,
            column_config={
                "filename": "文件名",
                "bill_type": "账单类型",
                "upload_timestamp": "上传日期"
            },
            hide_index=True
        )
    else:
        st.info("尚未上传任何账单文件")

    st.subheader("上传账单文件")
    with st.form("upload_form"):
        uploaded_file = st.file_uploader("请选择账单文件", type=["csv", "xls", "xlsx"])
        selected_bill_type = st.selectbox("选择账单类型", BILL_TYPES)
        submit_button = st.form_submit_button("上传")
        if submit_button:
            upload_result = bill_file_uploader(uploaded_file, selected_bill_type)
            if upload_result["status"]:
                st.success(upload_result["message"])
            else:
                st.session_state.bill_file_content = None # Clear bill content on error/warning
                st.warning(upload_result["message"])
            st.rerun()



if __name__ == "__main__":
    main()