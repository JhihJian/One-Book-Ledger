import unittest
from one_book_ledger.bill_parser.field_convert import convert_date_format,remove_sign,get_income_or_expense

class TestConvertDateFormat(unittest.TestCase):

    def test_convert_date_format_valid_date(self):
        self.assertEqual(convert_date_format('20250105'), '2025-01-05 00:00:00')
        self.assertEqual(convert_date_format('20241231'), '2024-12-31 00:00:00')

    def test_convert_date_format_invalid_date(self):
        self.assertIsNone(convert_date_format('20251305'))  # 无效的月份
        self.assertIsNone(convert_date_format('20250230'))  # 无效的日期
        self.assertIsNone(convert_date_format('20250105a')) # 包含非数字字符

    def test_convert_date_format_empty_string(self):
        self.assertIsNone(convert_date_format(''))

    def test_convert_date_format_with_time(self):
        self.assertEqual(convert_date_format('20250105', '21:54:25'), '2025-01-05 21:54:25')
        self.assertEqual(convert_date_format('20241231', '08:00:00'), '2024-12-31 08:00:00')

    def test_convert_date_format_invalid_time(self):
        self.assertIsNone(convert_date_format('20250105', '25:00:00'))  # 无效的小时
        self.assertIsNone(convert_date_format('20250105', '12:60:00'))  # 无效的分钟
        self.assertIsNone(convert_date_format('20250105', '12:34:56a')) # 包含非数字字符

    def test_remove_sign_positive(self):
        self.assertEqual(remove_sign('+100.00'), '100.00')
        self.assertEqual(remove_sign('123.45'), '123.45')

    def test_remove_sign_negative(self):
        self.assertEqual(remove_sign('-59.90'), '59.90')
        self.assertEqual(remove_sign('-0'), '0.00')

    def test_remove_sign_zero(self):
        self.assertEqual(remove_sign('0.00'), '0.00')
        self.assertEqual(remove_sign('0'), '0.00')

    def test_remove_sign_invalid(self):
        self.assertIsNone(remove_sign('abc'))
        self.assertIsNone(remove_sign(''))  # 空字符串

    def test_get_income_or_expense_positive(self):
        self.assertEqual(get_income_or_expense(100.00), '支出')
        self.assertEqual(get_income_or_expense(123.45), '支出')
        self.assertEqual(get_income_or_expense(100), '支出') # 测试整数

    def test_get_income_or_expense_negative(self):
        self.assertEqual(get_income_or_expense(-59.90), '收入')
        self.assertEqual(get_income_or_expense(-123.456), '收入')
        self.assertEqual(get_income_or_expense(-10), '收入') # 测试整数

    def test_get_income_or_expense_zero(self):
        self.assertEqual(get_income_or_expense(0.00), '其他')
        self.assertEqual(get_income_or_expense(0), '其他') # 测试整数

    def test_get_income_or_expense_invalid(self):
        self.assertIsNone(get_income_or_expense('abc'))
        self.assertIsNone(get_income_or_expense(''))  # 空字符串

    def test_get_income_or_expense_string(self):  # 测试字符串输入
        self.assertEqual(get_income_or_expense('100.00'), '支出')
        self.assertEqual(get_income_or_expense('-59.90'), '收入')
        self.assertEqual(get_income_or_expense('0.00'), '其他')

if __name__ == '__main__':
    unittest.main()