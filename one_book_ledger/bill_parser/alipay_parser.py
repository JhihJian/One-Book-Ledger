from one_book_ledger.bill_parser.common_paser import parse


def parse_alipay_csv(input_f):
    """解析支付宝CSV文件。

    Args:
        input_f (str): 输入CSV文件路径。
    """
    encoding = 'gbk'
    skip_lines = 24
    column_mapping = [
        ('交易时间', '交易时间', None),
        ('交易分类', '交易分类', None),  # 使用映射函数
        ('交易对方', '交易对方', None),
        ('商品说明', '交易说明', None),
        ('金额', '交易金额', None),
        ('收/支', '收/支', None),
        ('收/付款方式', '收/付款账户', None),
        ('交易状态', '交易状态', None)
    ]
    extra_columns = {'交易渠道': '支付宝'}
    return parse(input_f, column_mapping, extra_columns, encoding, skip_lines)


