# -*- coding: utf-8 -*-
"""
通用工具函数模块
"""
import datetime
import logging
import re
import openpyxl
import csv # 导入 csv 模块

# ... (之前的工具函数代码，例如 parse_amount, parse_datetime, standardize_transaction_type 和 parse_xls_bill 等) ...


def parse_csv_bill(csv_filepath, column_name_mapping, encoding='utf-8'):
    """
    通用 CSV 账单文件解析函数.

    Args:
        csv_filepath (str): CSV 账单文件路径.
        column_name_mapping (dict): CSV 列名到通用字段名的映射字典.
                                        例如: {'交易时间': '日期', '交易类型': '交易摘要', ...}
        encoding (str): CSV 文件编码，默认为 'utf-8'.

    Returns:
        list: 账单信息列表，每个元素为字典。
              如果解析过程中出现错误，返回 None.
    """
    bill_data = []
    try:
        with open(csv_filepath, 'r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile) # 使用 DictReader 以表头行作为字典的 key

            if not reader.fieldnames:
                logging.error(f"错误: CSV 文件缺少表头行: {csv_filepath}") # 使用 logging 输出错误
                return None

            # 获取列索引 (使用表头行 fieldnames，不需要手动查找索引)
            column_indices = {} #  虽然 DictReader 不需要列索引，但为了保持结构一致，这里保留 column_indices 字典
            for col_name_csv, field_name in column_name_mapping.items():
                if col_name_csv not in reader.fieldnames:
                    logging.warning(f"警告: CSV 文件缺少列: {col_name_csv}") # 使用 logging 输出警告
                    column_indices[field_name] = None #  如果找不到列，则设置为 None
                else:
                    column_indices[field_name] = col_name_csv #  对于 DictReader，列索引直接使用列名

            # 遍历数据行
            for row in reader: # reader is already an iterator, no need for range()
                bill_item = {}
                try:
                    for field_name, col_name_csv in column_name_mapping.items():
                        if col_name_csv is not None and col_name_csv in row: # 检查列是否存在于当前行
                            bill_item[field_name] = row[col_name_csv] #  直接使用列名从 row 字典中取值
                    bill_data.append(bill_item)

                except Exception as e:
                    logging.warning(f"解析 CSV 账单行出错 (行号: 未知, CSV DictReader 无行号): {e}") # 使用 logging 输出警告，CSV DictReader 没有直接的行号
                    continue # 跳过错误行

            return bill_data

    except FileNotFoundError:
        logging.error(f"错误: 文件未找到: {csv_filepath}") # 使用 logging 输出错误
        return None
    except Exception as e:
        logging.error(f"解析 CSV 文件出错: {e}") # 使用 logging 输出错误
        return None