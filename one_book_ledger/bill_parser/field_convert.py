import datetime

def convert_date_format(date_str, time_str="00:00:00"):
    """
    将'YYYYMMDD'格式的日期字符串转换为'YYYY-MM-DD HH:MM:SS'格式的日期时间字符串。

    Args:
        date_str (str): 'YYYYMMDD'格式的日期字符串，例如 '20250105'。
        time_str (str, optional): 'HH:MM:SS'格式的时间字符串，默认为 '00:00:00'。

    Returns:
        str: 'YYYY-MM-DD HH:MM:SS'格式的日期时间字符串，例如 '2025-01-05 00:00:00'。
           如果输入日期字符串格式不正确，则返回 None。
    """
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y%m%d').date()  # 将字符串转换为date对象
        time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S').time() # 将字符串转换为time对象
        datetime_obj = datetime.datetime.combine(date_obj, time_obj) #date和time结合
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')  # 将date对象格式化为指定字符串
    except ValueError:
        return None  # 返回 None 表示日期字符串格式不正确

def remove_sign(amount_str):
    """
    去除金额字符串中的正负号，并保留两位小数。

    Args:
        amount_str (str): 金额字符串，例如 '-59.90' 或 '+100.00'。

    Returns:
        str: 去除正负号后的金额字符串，保留两位小数，例如 '59.90' 或 '100.00'。
           如果输入字符串不是有效的金额格式，则返回 None。
    """
    try:
        amount = float(amount_str)  # 尝试将字符串转换为浮点数
        return "{:.2f}".format(abs(amount))  # 取绝对值，格式化为保留两位小数的字符串
    except ValueError:
        return None  # 返回 None 表示输入字符串格式不正确

def get_income_or_expense(amount):
    """
    根据金额的正负号返回“支出”或“收入”。

    Args:
        amount (float or int or str): 金额，可以是浮点数、整数或字符串。

    Returns:
        str: 如果金额为正，则返回“支出”；如果金额为负，则返回“收入”。
           如果金额为零，则返回“其他”。
           如果输入金额格式不正确，则返回 None。

    额外说明：
        正数表示账户支出，负数表示收入。
    """
    try:
        amount = float(amount)  # 尝试将输入转换为浮点数
        if amount > 0:
            return "支出"  # 正数表示支出
        elif amount < 0:
            return "收入"  # 负数表示收入
        else:
            return "其他"  # 金额为零
    except ValueError:
        return None  # 金额格式不正确