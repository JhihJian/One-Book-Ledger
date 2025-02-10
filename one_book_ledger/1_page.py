import streamlit as st
from one_book_ledger.database_helper import DatabaseHelper

def main():
    st.title("One-Book-Ledger - 账单文件列表")

    db_helper = DatabaseHelper()
    bill_files_data = db_helper.get_bill_files() # 获取账单文件列表数据 (列表字典格式)
    db_helper.close_connection()

    if bill_files_data:
        st.subheader("已上传账单文件")
        #  使用 st.dataframe 展示数据
        st.dataframe(
            bill_files_data, #  传入列表字典数据
            column_config={ #  配置列显示名称
                "filename": "文件名",
                "bill_type": "账单类型",
                "upload_timestamp": "上传日期"
            },
            hide_index=True #  隐藏索引列
        )
    else:
        st.info("尚未上传任何账单文件")

if __name__ == "__main__":
    main()