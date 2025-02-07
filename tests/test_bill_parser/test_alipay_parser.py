import unittest
import os
import csv
from one_book_ledger.bill_parser.alipay_parser import parse_alipay_csv_bill
from datetime import datetime

class TestAlipayParser(unittest.TestCase):

    def setUp(self):
        # 创建测试 CSV 文件 (内容来自假设的支付宝账单 CSV 格式)
        self.test_csv_filename = 'alipay_bill_test.csv'
        self.test_csv_filepath = os.path.join('tests', 'test_bill_parser', self.test_csv_filename)

        #  使用 csv 模块创建 CSV 文件并写入测试数据
        with open(self.test_csv_filepath, 'w', encoding='gbk', newline='') as csvfile: #  假设编码为 gbk，根据实际情况调整
            writer = csv.writer(csvfile)
            # 写入表头行 (假设的支付宝 CSV 表头行，需要根据实际文件调整)
            header_row = ['交易时间', '交易类型', '收/支', '金额', '商品名称', '交易对方', '备注']
            writer.writerow(header_row)
            # 写入数据行 (示例数据，需要根据实际情况调整)
            data_rows = [
                ['2025-01-05 10:00:00', '消费', '支出', '-59.90', '商品A', '淘宝店铺A', '备注1'],
                ['2025-01-05 12:00:00', '充值', '收入', '12.00', '充值', '支付宝', '备注2'],
                ['2025-01-06 14:00:00', '转账', '支出', '-244.00', '转账', '用户B', '备注3'],
                ['2025-01-07 16:00:00', '红包', '收入', '55.00', '红包', '用户C', '备注4'],
            ]
            writer.writerows(data_rows)

        # 确保 tests/test_bill_parser 目录存在
        os.makedirs(os.path.dirname(self.test_csv_filepath), exist_ok=True)


        # 预期的解析结果 (根据测试 CSV 内容手动创建 - 需要根据 CSV 文件内容调整)
        self.expected_bill_data = [
            {
                '账户': '支付宝',
                '日期': datetime(2025, 1, 5, 10, 0, 0), # 日期格式需要与 CSV 文件中的日期格式一致
                '交易摘要': '消费', # 假设 "交易类型" 作为交易摘要
                '交易对方': '淘宝店铺A',
                '商品说明': '商品A',
                '金额': -59.90,
                '收/支类型': '支出',
                '支付方式': '支付宝',
                '交易状态': '交易成功',
                '备注': '备注1',
                '类型': '消费', #  标准化后的交易类型
            },
            {
                '账户': '支付宝',
                '日期': datetime(2025, 1, 5, 12, 0, 0),
                '交易摘要': '充值',
                '交易对方': '支付宝',
                '商品说明': '充值',
                '金额': 12.00,
                '收/支类型': '收入',
                '支付方式': '支付宝',
                '交易状态': '交易成功',
                '备注': '备注2',
                '类型': '充值', #  标准化后的交易类型
            },
            {
                '账户': '支付宝',
                '日期': datetime(2025, 1, 6, 14, 0, 0),
                '交易摘要': '转账',
                '交易对方': '用户B',
                '商品说明': '转账',
                '金额': -244.00,
                '收/支类型': '支出',
                '支付方式': '支付宝',
                '交易状态': '交易成功',
                '备注': '备注3',
                '类型': '转账', #  标准化后的交易类型
            },
            {
                '账户': '支付宝',
                '日期': datetime(2025, 1, 7, 16, 0, 0),
                '交易摘要': '红包',
                '交易对方': '用户C',
                '商品说明': '红包',
                '金额': 55.00,
                '收/支类型': '收入',
                '支付方式': '支付宝',
                '交易状态': '交易成功',
                '备注': '备注4',
                '类型': '红包', #  标准化后的交易类型
            },
        ]

    def tearDown(self):
        # 清理测试 CSV 文件
        if os.path.exists(self.test_csv_filepath):
            os.remove(self.test_csv_filepath)

    def test_parse_alipay_csv_bill(self):
        """
        测试 parse_alipay_csv_bill 函数能否正确解析支付宝 CSV 账单文件.
        """
        bill_data = parse_alipay_csv_bill(self.test_csv_filepath)

        self.assertIsNotNone(bill_data, "解析结果不应为 None")
        self.assertIsInstance(bill_data, list, "解析结果应为列表")
        self.assertEqual(len(bill_data), 4, "解析结果列表长度应为 4")

        # 逐项比对解析结果和预期结果
        for i, expected_item in enumerate(self.expected_bill_data):
            actual_item = bill_data[i]
            self.assertEqual(actual_item['日期'], expected_item['日期'], f"第 {i+1} 项 日期不匹配")
            self.assertEqual(actual_item['交易摘要'], expected_item['交易摘要'], f"第 {i+1} 项 交易摘要不匹配")
            self.assertEqual(actual_item['交易对方'], expected_item['交易对方'], f"第 {i+1} 项 交易对方不匹配")
            self.assertEqual(actual_item['商品说明'], expected_item['商品说明'], f"第 {i+1} 项 商品说明不匹配")
            self.assertAlmostEqual(actual_item['金额'], expected_item['金额'], places=2, msg=f"第 {i+1} 项 金额不匹配")
            self.assertEqual(actual_item['收/支类型'], expected_item['收/支类型'], f"第 {i+1} 项 收/支类型不匹配")
            self.assertEqual(actual_item['支付方式'], expected_item['支付方式'], f"第 {i+1} 项 支付方式不匹配")
            self.assertEqual(actual_item['交易状态'], expected_item['交易状态'], f"第 {i+1} 项 交易状态不匹配")
            self.assertEqual(actual_item['备注'], expected_item['备注'], f"第 {i+1} 项 备注不匹配")
            self.assertEqual(actual_item['类型'], expected_item['类型'], f"第 {i+1} 项 类型不匹配")


    def test_parse_alipay_csv_bill_file_not_found(self):
        """
        测试 parse_alipay_csv_bill 函数在文件未找到时是否返回 None。
        """
        bill_data = parse_alipay_csv_bill('non_existent_alipay_file.csv') # 文件名改为 non_existent_alipay_file.csv，更清晰
        self.assertIsNone(bill_data, "文件未找到时应返回 None")


if __name__ == '__main__':
    unittest.main()