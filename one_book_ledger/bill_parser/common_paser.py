import os
from one_book_ledger.bill_parser.utils import (
    read_csv_to_dataframe,
    read_excel_to_dataframe,  # 导入 read_excel_to_dataframe
    transform_dataframe,
    add_constant_column,
)


def parse(input_f, column_mapping, extra_columns=None, encoding=None, skip_lines=0):
    """
    通用CSV/Excel解析方法，根据文件后缀名判断调用不同的读取函数。

    Args:
        input_f (str): 输入文件路径。
        column_mapping (list): 列映射关系列表，包含三元组 (原始列名, 目标列名, 转换函数)。
        extra_columns (dict, optional): 额外的常量列，键为列名，值为常量值。默认为None。
        encoding (str, optional): 文件编码格式。默认为 None，表示自动检测。
        skip_lines (int, optional): 需要跳过的行数。默认为 0。
    """
    try:
        file_extension = os.path.splitext(input_f)[1].lower()  # 获取文件后缀名并转换为小写

        if file_extension == '.csv':
            df = read_csv_to_dataframe(input_f, encoding=encoding, skip_lines=skip_lines)
        elif file_extension == '.xlsx' or file_extension == '.xls':  # 支持 xlsx 和 xls 格式
            df = read_excel_to_dataframe(input_f, skiprows=skip_lines)  # 默认读取第一个 sheet
        else:
            print(f"不支持的文件格式: {file_extension}")
            return

        if df is None:
            return

        transformed_df = transform_dataframe(df, column_mapping)

        if extra_columns:
            for col_name, value in extra_columns.items():
                transformed_df = add_constant_column(transformed_df, col_name, value)

        return transformed_df

    except Exception as e:
        print(f"解析文件出错: {e}")
