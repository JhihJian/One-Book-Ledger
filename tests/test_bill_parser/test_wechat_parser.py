import unittest
import pandas as pd
from one_book_ledger.bill_parser.wechat_parser import parse_wechat_csv,convert_refund_status  # 假设模块路径
from one_book_ledger.bill_parser.utils import write_dataframe_to_csv


class TestConvertRefundStatus(unittest.TestCase):

    def test_convert_refund_status_with_amount(self):
        self.assertEqual(convert_refund_status("已退款￥1.51"), "已退款")
        self.assertEqual(convert_refund_status("已退款￥10.00"), "已退款")

    def test_convert_refund_status_without_amount(self):
        self.assertEqual(convert_refund_status("未退款"), "未退款")
        self.assertEqual(convert_refund_status("已退款（部分）￥0.50"), "已退款")

    def test_convert_refund_status_empty_string(self):
        self.assertEqual(convert_refund_status(""), "")

    def test_convert_refund_status_none(self):
        self.assertIsNone(convert_refund_status(None))  # 或 self.assertEqual(convert_refund_status(None), None)


if __name__ == '__main__':
    # unittest.main()

    # 替换为您的CSV文件路径
    input_file = 'C:\\Users\\jhihjian\\Desktop\\0-生活\\账单\\20250105-20250204\\20250105-20250204微信账单.csv'
    output_file = 'bill_data.csv'  # 替换为您想要输出的文件路径
    df = parse_wechat_csv(input_file)
    write_dataframe_to_csv(df, output_file)
