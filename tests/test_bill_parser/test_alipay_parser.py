import unittest
import pandas as pd
from one_book_ledger.bill_parser.alipay_parser import parse_alipay_csv  # 假设模块路径
from one_book_ledger.bill_parser.utils import write_dataframe_to_csv


if __name__ == '__main__':
    # 替换为您的支付宝CSV文件路径
    input_file = 'C:\\Users\\jhihjian\\Desktop\\0-生活\\账单\\20250105-20250204\\20250105-20250204支付宝账单.csv'
    output_file = 'bill_data.csv'  # 替换为您想要输出的文件路径
    df = parse_alipay_csv(input_file)
    write_dataframe_to_csv(df, output_file)
