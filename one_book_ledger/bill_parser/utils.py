import pandas as pd
import chardet

def auto_detect_encoding(file_path):
    """自动检测文件编码格式。

    Args:
        file_path (str): 文件路径。

    Returns:
        str: 检测到的编码格式，如果检测失败则返回 None。
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding_detection = chardet.detect(raw_data)
            if encoding_detection['encoding'] == 'GB2312':
                encoding_detection['encoding'] = 'gbk'
            return encoding_detection['encoding']
    except Exception:
        return None

def auto_skip_header_lines(file_path, encoding='utf-8', num_lines_to_check=100):
    """自动检测并确定需要跳过的非CSV格式行数。

    Args:
        file_path (str): 文件路径。
        encoding (str, optional): 文件编码格式。默认为 'utf-8'。
        num_lines_to_check (int, optional): 检查的行数，用于判断header行. 默认为 20.

    Returns:
        int: 需要跳过的行数。
    """
    skip_lines_auto = 0
    header_line_found = False
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            for i, line in enumerate(f):
                if i >= num_lines_to_check: # 只检查前 N 行
                    break
                if ',' in line.strip(): # 简单判断是否包含逗号，可能是CSV header
                    # 进一步判断是否是header行 (可以根据实际情况调整判断标准)
                    # 这里简单判断是否不是纯数字行，header通常包含文本
                    if not line.strip().replace(',', '').replace('.', '').replace('-', '').isdigit():
                        skip_lines_auto = i
                        header_line_found = True
                        break # 找到header行就停止
    except Exception:
        pass # 忽略读取文件可能发生的错误，返回默认值

    return skip_lines_auto


def read_csv_to_dataframe(file_path, skip_lines=0, encoding=None):
    """读取CSV文件并将其转换为DataFrame，自动识别编码和跳过非CSV格式行。

    Args:
        file_path (str): CSV文件路径。
        skip_lines (int, optional): 需要跳过的行数（文件头）。如果为 None，则自动检测。 默认为 0.
        encoding (str, optional): 文件编码格式。如果为 None，则自动检测。 默认为 None (自动检测)。

    Returns:
        pandas.DataFrame: 读取到的数据，以DataFrame形式返回。
        如果文件无法读取或处理，则返回None。
    """
    try:
        # 自动检测编码格式
        if encoding is None:
            detected_encoding = auto_detect_encoding(file_path)
            if detected_encoding:
                encoding = detected_encoding
            else:
                encoding = 'utf-8' # 默认编码


        # 自动检测跳过行数
        if skip_lines is None:
            skip_lines = auto_skip_header_lines(file_path, encoding=encoding)
        elif skip_lines == 0: # 如果用户显式设置为0，也尝试自动检测，但优先级低于用户手动设置的非0值
             skip_lines_auto_detected = auto_skip_header_lines(file_path, encoding=encoding)
             if skip_lines_auto_detected > 0 : # 只有自动检测到跳过行数大于0时才使用自动检测结果，否则保持用户设置的0
                 skip_lines = skip_lines_auto_detected


        df = pd.read_csv(file_path, skiprows=skip_lines, encoding=encoding)
        return df
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return None
    except pd.errors.ParserError:
        print(f"解析CSV文件出错：{file_path}")
        return None
    except UnicodeDecodeError:  # 处理编码错误
        print(f"解码CSV文件出错，请检查编码格式：{file_path}, 尝试其他编码或手动指定编码格式。")
        return None
    except Exception as e:
        print(f"发生未知错误：{e}")
        return None



def read_excel_to_dataframe(file_path,  skiprows=0, encoding=None):
    """
    读取 Excel 文件并将其转换为 DataFrame。

    Args:
        file_path (str): Excel 文件路径。
        skiprows (int, optional): 需要跳过的行数。默认为 0。

    Returns:
        pandas.DataFrame: 读取到的数据，以DataFrame形式返回。
        如果文件无法读取或处理，则返回 None。
    """
    try:
        df = pd.read_excel(
            file_path,
            skiprows=skiprows
        )
        return df
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return None
    except Exception as e:
        print(f"发生未知错误：{e}")
        return None


def transform_dataframe(df, column_mapping):
    """根据映射关系列表转换DataFrame列，并应用不同的字段转换方法。

    Args:
        df (pandas.DataFrame): 输入的DataFrame。
        column_mapping (list): 包含三元组的映射关系列表，
            每个三元组包含 (原始列名, 目标列名, 字段转换方法)。

    Returns:
        pandas.DataFrame: 转换后的DataFrame。
    """
    new_df = pd.DataFrame()
    for old_col, new_col, func in column_mapping:
        if old_col in df.columns:
            if callable(func):  # 检查是否为函数
                new_df[new_col] = df[old_col].apply(func)
            elif isinstance(func, dict):  # 检查是否为字典
                # 处理字典映射
                mapping_dict = func
                new_df[new_col] = df[old_col].map(mapping_dict).fillna(df[old_col])  # 保留未映射的值
            elif func is None:  # 如果没有转换函数，则直接复制列
                new_df[new_col] = df[old_col]
            else:
                print(f"字段 {old_col} 的转换方法无效。")

    return new_df


def write_dataframe_to_csv(df, output_file):
    """将DataFrame写入CSV文件。

    Args:
        df (pandas.DataFrame): 要写入的DataFrame。
        output_file (str): 输出CSV文件路径。
    """
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"写入CSV文件出错：{e}")


def add_constant_column(df, column_name, value):
    """
    向DataFrame中添加一个常量字段。

    Args:
        df (pandas.DataFrame): 输入的DataFrame。
        column_name (str): 新字段的名称。
        value (any): 常量值。

    Returns:
        pandas.DataFrame: 添加了常量字段的DataFrame。
    """

    df[column_name] = value  # 直接赋值，pandas会自动广播到每一行
    return df


