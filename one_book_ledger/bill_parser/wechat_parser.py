from one_book_ledger.bill_parser.common_paser import parse
import re


def convert_refund_status(text):
    """
    将包含退款金额的退款状态字符串转换为简洁的退款状态字符串。

    Args:
        text (str): 包含退款金额的退款状态字符串，例如 "已退款￥1.51"。

    Returns:
        str: 简洁的退款状态字符串，例如 "已退款"。
           如果输入字符串不符合预期的格式，则返回原始字符串。
    """
    if text is None:
        return None

    if "已退款" in text:
        return "已退款"
    else:
        return text


def parse_wechat_csv(input_f):
    """解析微信CSV文件。

    Args:
        input_f (str): 输入CSV文件路径。
    """
    encoding = 'utf-8'
    skip_lines = 16
    column_mapping = [
        ('交易时间', '交易时间', None),
        ('交易类型', '交易分类', None),  # 使用映射函数
        ('交易对方', '交易对方', None),
        ('商品', '交易说明', None),
        ('金额(元)', '交易金额', None),
        ('收/支', '收/支', None),
        ('支付方式', '收/付款账户', None),
        ('当前状态', '交易状态', None)
    ]
    extra_columns = {'统计账单': '微信'}
    df = parse(input_f, column_mapping, extra_columns, encoding, skip_lines)

    # 特殊处理 1. 将 {'收/付款账户'：'/','交易状态':'已存入零钱'} 处理为 {'收/付款账户'：'零钱','交易状态':'交易成功'}
    df.loc[df['交易状态'] == '已存入零钱', '收/付款账户'] = '零钱'  # 使用 .loc 定位并修改
    df.loc[df['交易状态'] == '已存入零钱', '交易状态'] = '交易成功'
    return df
