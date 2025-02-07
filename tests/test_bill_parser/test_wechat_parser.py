import unittest
import os
from one_book_ledger.bill_parser.wechat_parser import parse_wechat_csv_bill
from datetime import datetime

class TestWechatParser(unittest.TestCase):

    def setUp(self):
        # 创建测试 CSV 文件 (内容来自用户提供的微信账单示例数据)
        self.test_csv_filename = 'wechat_bill_test.csv'
        self.test_csv_filepath = os.path.join('tests', 'test_bill_parser', self.test_csv_filename)
        test_csv_content = """微信支付账单明细,,,,,,,,
微信昵称：[正明],,,,,,,,
起始时间：[2025-01-05 00:00:00] 终止时间：[2025-02-04 23:59:59],,,,,,,,
导出类型：[全部],,,,,,,,
导出时间：[2025-02-06 16:01:11],,,,,,,,
,,,,,,,,
共65笔记录,,,,,,,,
收入：22笔 666.63元,,,,,,,,
支出：43笔 1618.75元,,,,,,,,
中性交易：0笔 0.00元,,,,,,,,
注：,,,,,,,,
1. 充值/提现/理财通购买/零钱通存取/信用卡还款等交易，将计入中性交易,,,,,,,,
2. 本明细仅展示当前账单中的交易，不包括已删除的记录,,,,,,,,
3. 本明细仅供个人对账使用,,,,,,,,
,,,,,,,,
----------------------微信支付账单明细列表--------------------,,,,,,,,
交易时间,交易类型,交易对方,商品,收/支,金额(元),支付方式,当前状态,交易单号,商户单号,备注
2025-02-04 21:54:25,商户消费,肯德基,"KFC_PREWX10012462029269016928301",支出,¥9.00,浦发银行信用卡(5683),支付成功,4200002511202502048273437886\t,WX10012462029269016928301\t,"/"
2025-02-04 21:52:26,商户消费,肯德基,"KFC_PREWX10012462027717413855696",支出,¥69.00,浦发银行信用卡(5683),支付成功,4200002512202502046003653177\t,WX10012462027717413855696\t,"/"
2025-02-04 12:03:41,商户消费,起点中文网,"充值1200起点币",支出,¥12.00,浦发银行信用卡(5683),支付成功,4200002556202502049685759348\t,7467409728861974798\t,"/"
2025-02-03 09:30:03,商户消费,起点中文网,"充值600起点币",支出,¥6.00,浦发银行信用卡(5683),支付成功,4200002563202502036294258474\t,7466999052697346956\t,"/"
"""
        # 确保 tests/test_bill_parser 目录存在
        os.makedirs(os.path.dirname(self.test_csv_filepath), exist_ok=True)
        with open(self.test_csv_filepath, 'w', encoding='utf-8') as f:
            f.write(test_csv_content)

        # 预期的解析结果 (根据测试 CSV 内容手动创建),  与最新的 BILL_ITEM_STRUCTURE 对应
        self.expected_bill_data = [
            {
                '日期': datetime(2025, 2, 4, 21, 54, 25),
                '类型': '商户消费',
                '交易对方': '肯德基',
                '商品说明': 'KFC_PREWX10012462029269016928301',
                '收/支类型': '支出',
                '金额': 9.00,
                '支付方式': '浦发银行信用卡(5683)',
                '交易状态': '支付成功',
                '交易订单号': '4200002511202502048273437886\t',
                '商家订单号': 'WX10012462029269016928301\t',
                '备注_原始': '/',
                '账户': '微信', # 账户类型是固定的，在代码中添加
                '备注': '/', #  微信账单备注直接使用原始备注
            },
            {
                '日期': datetime(2025, 2, 4, 21, 52, 26),
                '类型': '商户消费',
                '交易对方': '肯德基',
                '商品说明': 'KFC_PREWX10012462027717413855696',
                '收/支类型': '支出',
                '金额': 69.00,
                '支付方式': '浦发银行信用卡(5683)',
                '交易状态': '支付成功',
                '交易订单号': '4200002512202502046003653177\t',
                '商家订单号': 'WX10012462027717413855696\t',
                '备注_原始': '/',
                '账户': '微信', # 账户类型是固定的，在代码中添加
                '备注': '/', #  微信账单备注直接使用原始备注
            },
            {
                '日期': datetime(2025, 2, 4, 12, 3, 41),
                '类型': '商户消费',
                '交易对方': '起点中文网',
                '商品说明': '充值1200起点币',
                '收/支类型': '支出',
                '金额': 12.00,
                '支付方式': '浦发银行信用卡(5683)',
                '交易状态': '支付成功',
                '交易订单号': '4200002556202502049685759348\t',
                '商家订单号': '7467409728861974798\t',
                '备注_原始': '/',
                '账户': '微信', # 账户类型是固定的，在代码中添加
                '备注': '/', #  微信账单备注直接使用原始备注
            },
            {
                '日期': datetime(2025, 2, 3, 9, 30, 3),
                '类型': '商户消费',
                '交易对方': '起点中文网',
                '商品说明': '充值600起点币',
                '收/支类型': '支出',
                '金额': 6.00,
                '支付方式': '浦发银行信用卡(5683)',
                '交易状态': '支付成功',
                '交易订单号': '4200002563202502036294258474\t',
                '商家订单号': '7466999052697346956\t',
                '备注_原始': '/',
                '账户': '微信', # 账户类型是固定的，在代码中添加
                '备注': '/', #  微信账单备注直接使用原始备注
            },
        ]

    def tearDown(self):
        # 清理测试 CSV 文件
        if os.path.exists(self.test_csv_filepath):
            os.remove(self.test_csv_filepath)

    def test_parse_wechat_csv_bill(self):
        """
        测试 parse_wechat_csv_bill 函数能否正确解析微信 CSV 账单文件。
        """
        bill_data = parse_wechat_csv_bill(self.test_csv_filepath)

        self.assertIsNotNone(bill_data, "解析结果不应为 None")
        self.assertIsInstance(bill_data, list, "解析结果应为列表")
        self.assertEqual(len(bill_data), 4, "解析结果列表长度应为 4") # 根据测试 CSV 文件中的有效交易记录数调整

        # 逐项比对解析结果和预期结果 (比对所有交易记录)
        for i, expected_item in enumerate(self.expected_bill_data):
            actual_item = bill_data[i]
            self.assertEqual(actual_item['日期'], expected_item['日期'], f"第 {i+1} 项 日期不匹配")
            self.assertEqual(actual_item['类型'], expected_item['类型'], f"第 {i+1} 项 类型不匹配")
            self.assertEqual(actual_item['交易对方'], expected_item['交易对方'], f"第 {i+1} 项 交易对方不匹配")
            self.assertEqual(actual_item['商品说明'], expected_item['商品说明'], f"第 {i+1} 项 商品说明不匹配")
            self.assertEqual(actual_item['收/支类型'], expected_item['收/支类型'], f"第 {i+1} 项 收/支类型不匹配")
            self.assertAlmostEqual(actual_item['金额'], expected_item['金额'], places=2, msg=f"第 {i+1} 项 金额不匹配") # 使用 assertAlmostEqual 比较浮点数
            self.assertEqual(actual_item['支付方式'], expected_item['支付方式'], f"第 {i+1} 项 支付方式不匹配")
            self.assertEqual(actual_item['交易状态'], expected_item['交易状态'], f"第 {i+1} 项 交易状态不匹配")
            self.assertEqual(actual_item['交易订单号'], expected_item['交易订单号'], f"第 {i+1} 项 交易订单号不匹配")
            self.assertEqual(actual_item['商家订单号'], expected_item['商家订单号'], f"第 {i+1} 项 商家订单号不匹配")
            self.assertEqual(actual_item['备注_原始'], expected_item['备注_原始'], f"第 {i+1} 项 备注_原始不匹配")
            self.assertEqual(actual_item['账户'], expected_item['账户'], f"第 {i+1} 项 账户不匹配")
            self.assertEqual(actual_item['备注'], expected_item['备注'], f"第 {i+1} 项 备注不匹配")


    def test_parse_wechat_csv_bill_file_not_found(self):
        """
        测试 parse_wechat_csv_bill 函数在文件未找到时是否返回 None。
        """
        bill_data = parse_wechat_csv_bill('non_existent_wechat_file.csv') #  文件名改为 non_existent_wechat_file.csv，更清晰
        self.assertIsNone(bill_data, "文件未找到时应返回 None")


if __name__ == '__main__':
    unittest.main()