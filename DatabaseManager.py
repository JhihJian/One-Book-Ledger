import pandas as pd
import sqlite3

class DatabaseManager:
    """
    用于管理 SQLite 数据库连接和 DataFrame 操作的类。
    """
    def __init__(self, db_name):
        """
        初始化 DatabaseManager 实例。

        参数:
        db_name (str): 数据库文件名 (例如: 'mydatabase.db')。
        """
        self.db_name = db_name
        self.conn = None  # 初始化连接为 None，在需要时建立

    def connect(self):
        """
        建立数据库连接。如果连接已存在，则不执行任何操作。
        """
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_name)
                print(f"成功连接到数据库 '{self.db_name}'")
            except sqlite3.Error as e:
                print(f"连接数据库时出错: {e}")
                self.conn = None  # 连接失败时重置为 None

    def close_connection(self):
        """
        关闭数据库连接。
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"数据库 '{self.db_name}' 连接已关闭")

    def save_df(self, df, table_name, if_exists='fail', index=False):
        """
        将 Pandas DataFrame 保存到数据库表。

        参数:
        df (pd.DataFrame): 要保存的 Pandas DataFrame。
        table_name (str): 表名。
        if_exists (str, 可选): 如果表已存在时的行为。
            - 'fail': 如果表存在，则引发 ValueError。
            - 'replace': 如果表存在，则替换它。
            - 'append': 如果表存在，则将数据追加到表中。 默认值为 'fail'。
        index (bool, 可选): 是否将 DataFrame 索引写入数据库。默认为 False。
        """
        self.connect()  # 确保连接已建立
        if self.conn: # 只有当连接成功建立时才执行后续操作
            try:
                df.to_sql(table_name, self.conn, if_exists=if_exists, index=index)
                print(f"DataFrame 已成功保存到数据库 '{self.db_name}' 的表 '{table_name}'")
            except ValueError as e:
                print(f"保存 DataFrame 时出错 (ValueError): {e}")
            except Exception as e: # 捕获其他可能的异常
                print(f"保存 DataFrame 时发生未知错误: {e}")


    def query_df(self, table_name, query=None):
        """
        从数据库表查询数据并返回 Pandas DataFrame。

        参数:
        table_name (str): 表名。
        query (str, 可选): SQL 查询语句 (例如: "SELECT * FROM mytable WHERE column1 > 10")。
            如果为 None，则查询整个表 ("SELECT * FROM table_name")。 默认为 None。

        返回:
        pd.DataFrame: 从数据库查询到的 Pandas DataFrame。
                      如果查询失败或表不存在，则返回空的 DataFrame。
        """
        self.connect() # 确保连接已建立
        if self.conn: # 只有当连接成功建立时才执行后续操作
            if query is None:
                query = f"SELECT * FROM {table_name}"
            try:
                df = pd.read_sql_query(query, self.conn)
                print(f"已从数据库 '{self.db_name}' 的表 '{table_name}' 成功查询 DataFrame")
                return df
            except pd.io.sql.DatabaseError as e:
                print(f"查询数据库时出错 (DatabaseError): {e}")
                return pd.DataFrame() # 返回空 DataFrame，而不是 None
            except sqlite3.OperationalError as e:
                print(f"操作数据库时出错 (OperationalError): {e}")
                return pd.DataFrame()
            except Exception as e: # 捕获其他可能的异常
                print(f"查询 DataFrame 时发生未知错误: {e}")
                return pd.DataFrame()
        else:
            return pd.DataFrame() # 如果连接失败，返回空 DataFrame

