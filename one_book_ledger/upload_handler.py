import os
import datetime
from database_helper import DatabaseHelper

# 资源文件存储目录
RESOURCES_DIR = "resources"
os.makedirs(RESOURCES_DIR, exist_ok=True)  # Ensure resources directory exists

# 预定义的账单类型 (Consider moving to database later)
BILL_TYPES = ["微信账单", "支付宝账单", "中信银行账单", "浦发银行账单"]

def generate_unique_filename(original_filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename, extension = os.path.splitext(original_filename)
    unique_filename = f"{filename}_{timestamp}{extension}"
    return unique_filename

def bill_file_uploader(uploaded_file, selected_bill_type):  # Remove Streamlit UI elements, accept arguments
    if uploaded_file is not None:
        original_filename = uploaded_file.name
        unique_filename = generate_unique_filename(original_filename)
        storage_path = os.path.join(RESOURCES_DIR, unique_filename)

        try:
            with open(storage_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            db_helper = DatabaseHelper()
            save_success = db_helper.save_bill_file_info(original_filename, selected_bill_type, storage_path)
            db_helper.close_connection()

            if save_success:
                return {"status": True, "message": f"文件 '{original_filename}' 上传成功，账单类型为：{selected_bill_type}"} # Return success dict
            else:
                return {"status": False, "message": f"文件 '{original_filename}' 上传成功，但保存文件信息到数据库失败！"} # Return failure dict

        except Exception as e_save:  # Catch file saving errors
            return {"status": False, "message": f"文件 '{original_filename}' 上传失败，错误: {e_save}"}  # Return failure dict

    else:
        return {"status": False, "message": "请先选择要上传的账单文件"}  # Return warning dict