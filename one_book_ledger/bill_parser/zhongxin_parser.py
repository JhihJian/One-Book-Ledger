from one_book_ledger.bill_parser.common_paser import parse
from one_book_ledger.bill_parser.field_convert import convert_date_format,get_income_or_expense,remove_sign


def extract_account(trade_summary):
    """
    从交易摘要中提取收付款账户。

    Args:
        trade_summary (str): 交易摘要字符串，例如 '财付通-起点中文网'。

    Returns:
        str: 收付款账户名称，例如 '财付通'。
           如果交易摘要不包含 '-'，则返回 None。
    """
    if '-' in trade_summary:
        return trade_summary.split('-')[0]
    else:
        return None

def extract_description(trade_summary):
    """
    从交易摘要中提取商品描述。

    Args:
        trade_summary (str): 交易摘要字符串，例如 '财付通-起点中文网'。

    Returns:
        str: 商品描述，例如 '起点中文网'。
           如果交易摘要不包含 '-'，则直接返回交易摘要。
    """

    if '-' in trade_summary:
        return trade_summary.split('-')[1]
    else:
        return trade_summary

def parse_zhongxin_csv(input_f):
    """解析中信银行信用卡账单excel文件。

    Args:
        input_f (str): 输入CSV文件路径。
    """
    encoding = 'gbk'
    skip_lines = 1
    column_mapping = [
        ('交易日期', '交易时间', convert_date_format),
        ('交易摘要', '收/付款账户', extract_account),  # 使用映射函数
        ('交易对方', '交易对方', None),
        ('交易摘要', '交易说明', extract_description),
        ('交易金额', '交易金额', remove_sign),
        ('交易金额', '收/支', get_income_or_expense)
    ]
    extra_columns = {'交易分类': '','交易状态': '','统计账单': '中信银行'}

    return parse(input_f, column_mapping, extra_columns, encoding, skip_lines)


