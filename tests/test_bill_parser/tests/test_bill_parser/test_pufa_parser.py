import unittest
from one_book_ledger.bill_parser.pufa_parser import extract_account,extract_description

class TestExtractFunctions(unittest.TestCase):

    def test_extract_account(self):
        self.assertEqual(extract_account('财付通-起点中文网'), '财付通')
        self.assertEqual(extract_account('支付宝-淘宝网'), '支付宝')
        self.assertEqual(extract_account('微信支付-京东商城'), '微信支付')
        self.assertEqual(extract_account('银行卡-美团外卖'), '银行卡')
        self.assertIsNone(extract_account('直接支付'))  # 不包含 '-'
        self.assertIsNone(extract_account('已退款￥1.51')) # 不包含 '-'
        self.assertIsNone(extract_account('')) # 空字符串

    def test_extract_description(self):
        self.assertEqual(extract_description('财付通-起点中文网'), '起点中文网')
        self.assertEqual(extract_description('支付宝-淘宝网'), '淘宝网')
        self.assertEqual(extract_description('微信支付-京东商城'), '京东商城')
        self.assertEqual(extract_description('银行卡-美团外卖'), '美团外卖')
        self.assertEqual(extract_description('直接支付'), '直接支付')  # 不包含 '-'
        self.assertEqual(extract_description('已退款￥1.51'), '已退款￥1.51') # 不包含 '-'
        self.assertEqual(extract_description(''), '') # 空字符串

if __name__ == '__main__':
    unittest.main()