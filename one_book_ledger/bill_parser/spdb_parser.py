# -*- coding: utf-8 -*-
"""
浦发银行账单解析模块 (XLS 格式)
"""
import datetime
import logging
import openpyxl #  需要安装 openpyxl 库: pip install openpyxl

from one_book_ledger.utils import parse_amount, parse_datetime, standardize_transaction_type, TransactionType

# -------------------------------- 浦发银行账单字段结构 ---------------------------------
#  基于提供的浦发银行账单 Excel 文件列名
SPDB_BILL_ITEM_STRUCTURE = {
    '交易日期': '日期',
    '记账日期': '记账日期', #  浦发银行账单特有字段
    '交易摘要': '交易摘要', #  浦发银行账单特有字段，更详细的交易描述
    '卡号末四位': '卡号末四位', #  浦发银行账单特有字段，可以忽略或者用于辅助信息
    '卡片类型': '卡片类型', #  浦发银行账单特有字段，例如 "主卡"
    '交易币种': '交易币种', #  浦发银行账单特有字段，默认为 "人民币"
    '交易金额': '金额',
}

# -------------------------------- XLS 数据行解析函数 (浦发银行账单) --------------------------------

def _parse_spdb_xls_data_rows(sheet, header_row):
    """
    解析浦发银行 XLS 账单文件的数据行，提取账单信息 (使用 SPDB_BILL_ITEM_STRUCTURE 驱动).

    Args:
        sheet (openpyxl.worksheet.worksheet.Worksheet): openpyxl worksheet 对象，已跳过非数据行。
        header_row (list): XLS 表头行列表。

    Returns:
        list: 账单信息列表，每个元素为字典。
              如果解析过程中出现错误，会在控制台输出警告信息，并跳过错误行。
    """
    bill_data = []
    spdb_column_name_mapping = { # 浦发银行 XLS 列名到结构化数据字段名的映射 (硬编码)
        '交易日期': '日期',
        '交易摘要': '交易摘要',
        '交易金额': '金额',
    }

    # 获取列索引 (根据中文表头名)
    column_indices = {}
    for col_name_spdb, field_name in spdb_column_name_mapping.items():
        try:
            column_indices[field_name] = header_row.index(col_name_spdb)
        except ValueError:
            logging.warning(f"警告: 浦发银行账单缺少列: {col_name_spdb}") #  使用 logging 输出警告
            column_indices[field_name] = None #  如果找不到列，则设置为 None

    # 从第二行开始遍历数据行 (第一行是表头)
    for row_index in range(2, sheet.max_row + 1): # openpyxl 行索引从 1 开始，这里从 2 开始
        bill_item = {'账户': '浦发银行'}  # 账户类型固定为浦发银行
        row_values = [cell.value for cell in sheet[row_index]] # 获取当前行所有单元格的值

        if not any(row_values): #  跳过空行
            continue

        try:
            #  日期 (交易日期)
            date_value = row_values[column_indices['日期']]
            bill_item['日期'] = parse_datetime(date_value, date_format='%Y%m%d') #  浦发银行账单日期格式为 YYYYMMDD

            # 交易摘要
            transaction_summary = row_values[column_indices['交易摘要']]
            bill_item['类型'] = standardize_transaction_type(transaction_summary) #  尝试从摘要中标准化交易类型
            bill_item['交易对方'] = transaction_summary #  交易对方默认为交易摘要
            bill_item['商品说明'] = transaction_summary #  商品说明也默认为交易摘要

            # 金额 (交易金额)
            amount_value = row_values[column_indices['金额']]
            bill_item['金额'] = parse_amount(str(amount_value)) #  浦发银行账单金额可能为数字或字符串，统一转为字符串处理

            #  固定值字段
            bill_item['收/支类型'] = '支出' if bill_item['金额'] < 0 else '收入' #  根据金额正负判断收支类型
            bill_item['支付方式'] = '浦发银行信用卡' #  支付方式固定为 浦发银行信用卡
            bill_item['交易状态'] = '交易成功' #  默认交易状态为成功
            bill_item['备注'] = '' #  浦发银行账单没有单独的备注列，默认为空

            bill_data.append(bill_item)

        except Exception as e:
            logging.warning(f"解析浦发银行账单行出错 (行号: {row_index}): {e}") #  使用 logging 输出警告, 并包含行号
            continue #  跳过解析错误的行


    return bill_data