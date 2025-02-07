import unittest
import pandas as pd
from one_book_ledger.bill_parser.utils import transform_dataframe  # 假设模块路径


class TestTransformDataFrame(unittest.TestCase):

    def test_transform_dataframe_with_functions(self):
        # 测试用例：使用函数进行转换
        data = {'姓名': ['张三', '李四', '王五'], '年龄': ['25', '30', '28']}
        df = pd.DataFrame(data)

        column_mapping = [
            ('姓名', 'Name', None),
            ('年龄', 'Age', self.convert_age)
        ]

        expected_data = {'Name': ['张三', '李四', '王五'], 'Age': [25, 30, 28]}
        expected_df = pd.DataFrame(expected_data)

        transformed_df = transform_dataframe(df, column_mapping)

        pd.testing.assert_frame_equal(transformed_df, expected_df)

    def test_transform_dataframe_with_dict(self):
        # 测试用例：使用字典进行转换
        data = {'性别': ['男', '女', '男']}
        df = pd.DataFrame(data)

        column_mapping = [
            ('性别', 'Gender', {'男': 'Male', '女': 'Female'})
        ]

        expected_data = {'Gender': ['Male', 'Female', 'Male']}
        expected_df = pd.DataFrame(expected_data)

        transformed_df = transform_dataframe(df, column_mapping)

        pd.testing.assert_frame_equal(transformed_df, expected_df)

    def test_transform_dataframe_with_none(self):
        # 测试用例：直接复制列
        data = {'城市': ['北京', '上海', '广州']}
        df = pd.DataFrame(data)

        column_mapping = [
            ('城市', 'City', None)
        ]

        expected_data = {'City': ['北京', '上海', '广州']}
        expected_df = pd.DataFrame(expected_data)

        transformed_df = transform_dataframe(df, column_mapping)

        pd.testing.assert_frame_equal(transformed_df, expected_df)

    def convert_age(self, age):  # 用于测试的年龄转换函数
        try:
            return int(age)
        except (ValueError, TypeError):
            return None


if __name__ == '__main__':
    unittest.main()
