import sqlite3
import datetime
import os

DATABASE_NAME = "bill_ledger.db"

class DatabaseHelper:
    def __init__(self):
        self.conn = self._connect_db()
        self._create_tables()
        self._insert_test_data()

    def _connect_db(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            return conn
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")
            return None

    def _create_tables(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bill_files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        bill_type TEXT NOT NULL,
                        storage_path TEXT NOT NULL,
                        upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bill_types (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        parser_config TEXT --  解析器配置，暂时留空
                    )
                """)
                self.conn.commit()
                print("数据表创建/检查 完成")
            except sqlite3.Error as e:
                print(f"数据表创建失败: {e}")

    def _insert_test_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            try:
                # #  测试账单类型数据
                # cursor.execute("INSERT OR IGNORE INTO bill_types (name) VALUES (?)", ("支付宝账单",))
                # cursor.execute("INSERT OR IGNORE INTO bill_types (name) VALUES (?)", ("微信账单",))
                # cursor.execute("INSERT OR IGNORE INTO bill_types (name) VALUES (?)", ("中信银行信用卡账单",))
                #
                # #  测试账单文件数据
                # cursor.execute("""
                #     INSERT OR IGNORE INTO bill_files (filename, bill_type, storage_path)
                #     VALUES (?, ?, ?)
                # """, ("alipay_202412.csv", "支付宝账单", "/path/to/alipay_202412.csv"))
                # cursor.execute("""
                #     INSERT OR IGNORE INTO bill_files (filename, bill_type, storage_path)
                #     VALUES (?, ?, ?)
                # """, ("wechat_202412.xlsx", "微信账单", "/path/to/wechat_202412.xlsx"))
                #
                # self.conn.commit()
                print("测试数据初始化完成")
            except sqlite3.Error as e:
                print(f"测试数据初始化失败: {e}")

    def get_bill_files(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT filename, bill_type, upload_timestamp FROM bill_files order by upload_timestamp desc") #  查询 upload_timestamp
                files = cursor.fetchall()
                #  将列表元组转换为列表字典
                bill_file_list = []
                for file in files:
                    bill_file_list.append({
                        "filename": file[0],
                        "bill_type": file[1],
                        "upload_timestamp": file[2] #  获取上传时间
                    })
                return bill_file_list # 返回列表字典
            except sqlite3.Error as e:
                print(f"获取账单文件列表失败: {e}")
                return []
        return []

    def get_bill_types(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM bill_types")
            types = cursor.fetchall()
            return [item[0] for item in types] #  返回账单类型名称列表
        return []

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def get_bill_types_with_details(self):  # 新增方法：获取账单类型详情
        if self.conn is not None:
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT id, name FROM bill_types")  # 查询 id 和 name
                bill_types = cursor.fetchall()
                #  转换为列表字典
                bill_type_list = []
                for bill_type in bill_types:
                    bill_type_list.append({
                        "id": bill_type[0],
                        "name": bill_type[1]
                    })
                return bill_type_list  # 返回包含 id 和 name 的列表字典
            except sqlite3.Error as e:
                print(f"获取账单类型列表失败: {e}")
                return []
        return []

    def save_bill_file_info(self, filename, bill_type, storage_path): #  Ensure this method is present and correctly spelled
        if self.conn is not None:
            cursor = self.conn.cursor()
            try:
                cursor.execute("INSERT INTO bill_files (filename, bill_type, storage_path) VALUES (?, ?, ?)",
                               (filename, bill_type, storage_path))
                self.conn.commit()
                print(f"文件信息保存成功: {filename}, 类型: {bill_type}, 路径: {storage_path}") #  添加日志
                return True #  返回 True 表示保存成功
            except sqlite3.Error as e:
                print(f"文件信息保存失败: {filename}, 错误: {e}") #  添加错误日志
            return False #  返回 False 表示保存失败
        return False #  数据库连接失败，返回 False
