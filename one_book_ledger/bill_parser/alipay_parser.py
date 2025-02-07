# -*- coding: utf-8 -*-
"""
支付宝账单解析模块 (CSV 格式)
"""
import logging

from one_book_ledger.utils.utils import parse_amount, parse_datetime, standardize_transaction_type, TransactionType
from one_book_ledger.utils.csv_bill_parser import parse_csv_bill # 导入 parse_csv_bill

# -------------------------------- 支付宝账单字段结构 (CSV 格式) ---------------------------------
ALIPAY_BILL_ITEM_STRUCTURE_CSV = { #  支付宝 CSV 账单列名及其对应的通用字段名
    '交易时间': '日期',          #  支付宝 CSV 列名 '交易时间' 映射到通用字段名 '日期'
    '交易类型': '交易摘要',        #  支付宝 CSV 列名 '交易类型' 映射到通用字段名 '交易摘要'
    '收/支': '收/支类型',         #  支付宝 CSV 列名 '收/支' 映射到通用字段名 '收/支类型'
    '金额': '金额',            #  支付宝 CSV 列名 '金额' 映射到通用字段名 '金额'
    '商品名称': '商品说明',        #  支付宝 CSV 列名 '商品名称' 映射到通用字段名 '商品说明'
    '交易对方': '交易对方',        #  支付宝 CSV 列名 '交易对方' 映射到通用字段名 '交易对方'
    '备注': '备注',            #  支付宝 CSV 列名 '备注' 映射到通用字段名 '备注'
    # ... (如果支付宝 CSV 账单还有其他需要解析的列，可以继续在此处添加映射关系) ...
}


# -------------------------------- 主解析函数 (支付宝账单 CSV) --------------------------------

def parse_alipay_csv_bill(csv_filepath):
    """
    解析支付宝 CSV 账单文件，提取账单信息 (使用通用 CSV 解析函数).

    Args:
        csv_filepath (str): 支付宝账单 CSV 文件路径.

    Returns:
        list: 账单信息列表，每个元素为字典。
              如果解析过程中出现错误，返回 None。
    """
    alipay_column_name_mapping_csv = { #  支付宝 CSV 列名到通用字段名的映射 (与 ALIPAY_BILL_ITEM_STRUCTURE_CSV 相同，但作为局部变量在函数内部定义)
        '交易时间': '日期',
        '交易类型': '交易摘要',
        '收/支': '收/支类型',
        '金额': '金额',
        '商品名称': '商品说明',
        '交易对方': '交易对方',
        '备注': '备注',
        # ... (可以根据实际支付宝 CSV 文件表头行进行调整) ...
    }

    # 使用通用的 CSV 解析函数读取数据
    raw_bill_data = parse_csv_bill(csv_filepath, alipay_column_name_mapping_csv, encoding='gbk') #  指定 CSV 编码为 gbk (根据支付宝账单实际编码调整)
    if not raw_bill_data: #  如果通用解析函数返回 None，表示解析出错，直接返回 None
        return None

    bill_data = []
    for item in raw_bill_data:
        try:
            logging.debug(f"Raw Item from parse_csv_bill: {item}") #  输出从通用 CSV 解析函数获取的原始数据 (调试信息)
            bill_item = {
                '账户': '支付宝', # 账户类型固定为 支付宝
                '日期': parse_datetime(item.get('日期')) if item.get('日期') else None, # 解析日期，如果 '日期' 字段为空则为 None
                '交易摘要': item.get('交易摘要', '') or item.get('商品说明','') or item.get('交易对方', ''), # 交易摘要，按优先级取值
                '交易对方': item.get('交易对方', '') or item.get('商品说明',''), # 交易对方，按优先级取值
                '商品说明': item.get('商品说明', '') or item.get('交易类型', ''), # 商品说明，按优先级取值
                '金额': parse_amount(str(item.get('金额')), transaction_type=TransactionType.UNKNOWN) if item.get('金额') is not None else 0.0, # 解析金额，并指定交易类型为未知 (如果 '金额' 字段为空则为 0.0)
                '收/支类型': item.get('收/支类型', ''), # 直接获取 '收/支类型' 字段
                '支付方式': '支付宝', # 支付方式固定为 支付宝
                '交易状态': '交易成功', # 交易状态默认为 交易成功
                '备注': item.get('备注', ''), # 直接获取 '备注' 字段
                '类型': standardize_transaction_type(item.get('交易摘要', '')), #  从交易摘要标准化交易类型
            }
            bill_data.append(bill_item)
            logging.debug(f"Parsed Bill Item: {bill_item}") # 输出解析后的账单条目 (调试信息)
        except Exception as e:
            logging.warning(f"处理支付宝账单数据行出错: {e}") # 记录数据行处理错误
            continue #  跳过当前数据行，继续处理下一行

    return bill_data