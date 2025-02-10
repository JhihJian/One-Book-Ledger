import streamlit as st
import os
import sqlite3
import datetime # 用于生成唯一文件名 (可选)

# --- 数据库操作 ---
DATABASE_NAME = 'one_book_ledger.db'
BILL_TYPES_TABLE_NAME = 'bill_types'
UPLOAD_DIR = 'uploaded_bills' # 默认上传目录

def init_db():
    """初始化数据库和数据表"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {BILL_TYPES_TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            parser_config TEXT  # 预留字段，解析器配置
        )
    ''')
    conn.commit()
    conn.close()

def get_bill_types():
    """从数据库获取所有账单类型"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM {BILL_TYPES_TABLE_NAME}")
    bill_types = cursor.fetchall()
    conn.close()
    return [type[0] for type in bill_types] # 返回类型名称列表

def add_bill_type(name): # 暂时只添加名称
    """向数据库添加新的账单类型"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO {BILL_TYPES_TABLE_NAME} (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError: # 名称重复
        conn.close()
        return False

# --- 文件操作 ---
def save_uploaded_file(uploaded_file, bill_type_name):
    """保存上传的文件到指定目录"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR) # 创建上传目录如果不存在

    # 可以使用时间戳 + 原始文件名 避免冲突 (可选)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath, filename # 返回文件路径和文件名


# --- Streamlit 应用 ---
def main():
    st.title("One-Book-Ledger")

    # 初始化数据库和上传目录
    init_db()
    if 'bill_types' not in st.session_state:
        st.session_state['bill_types'] = get_bill_types()
    if 'uploaded_files' not in st.session_state:
        st.session_state['uploaded_files'] = [] #  文件名列表

    # 展示已上传文件列表
    if st.session_state['uploaded_files']:
        st.subheader("已上传账单文件")
        # 可以用 st.data_editor 也可以用简单的列表展示
        for filename in st.session_state['uploaded_files']:
            st.write(filename) # 简单展示文件名
    else:
        st.info("尚未上传任何账单文件")

    # 上传文件按钮
    if st.button("上传账单文件"):
        with st.expander("上传文件和选择账单类型", expanded=True): # 默认展开
            uploaded_file = st.file_uploader("上传账单文件", type=["csv", "xls", "xlsx", "txt"]) # 可以限制文件类型
            bill_type_options = ["创建账单类型"] + st.session_state['bill_types'] # 创建类型选项放前面
            selected_bill_type = st.selectbox("选择账单类型", bill_type_options)

            if uploaded_file is not None:
                if selected_bill_type == "创建账单类型":
                    #  TODO: 跳转到创建账单类型页面 (暂未实现)
                    st.warning("创建账单类型功能暂未实现，请稍后...")
                else:
                    # 保存文件
                    filepath, filename = save_uploaded_file(uploaded_file, selected_bill_type)
                    st.success(f"文件 '{filename}' 上传成功，已保存到: {filepath}")
                    st.session_state['uploaded_files'].append(filename) # 更新文件列表
                    #  TODO:  后续处理 -  例如解析文件,  加入统一账簿

if __name__ == "__main__":
    main()