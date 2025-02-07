import csv
from one_book_ledger.utils.utils import (
    parse_csv_row_to_dict,
    parse_datetime,
    parse_transaction_type,
    parse_amount_yuan_wechat
)

# -------------------------------- CSV 数据行解析函数 (微信账单) --------------------------------


def _parse_wechat_csv_data_rows(reader, header_row):
    """
    解析微信 CSV 账单文件的数据行，提取账单信息 (使用 BILL_ITEM_STRUCTURE 驱动).

    Args:
        reader (csv.reader): CSV 文件 reader 对象，已跳过非数据行。
        header_row (list): CSV 表头行列表。

    Returns:
        list: 账单信息列表，每个元素为字典。
              如果解析过程中出现错误，会在控制台输出警告信息，并跳过错误行。
    """
    bill_data = []
    csv_column_name_mapping = {  # 微信 CSV 列名到结构化数据字段名的映射 (硬编码)
        '交易时间': '日期',
        '交易类型': '类型',
        '交易对方': '交易对方',
        '商品': '商品说明',
        '收/支': '收/支类型',
        '金额(元)': '金额',
        '支付方式': '支付方式',
        '当前状态': '交易状态',
        '交易单号': '交易订单号',
        '商户单号': '商家订单号',
        '备注': '备注_原始',
    }

    for row in reader:
        row_dict = parse_csv_row_to_dict(row, header_row)
        if not row_dict:
            continue

        bill_item = {'账户': '微信'}   # 账户类型固定为微信

        for csv_column_name, field_name in csv_column_name_mapping.items():
            csv_value = row_dict.get(csv_column_name)
            field_value = csv_value  # 默认值

            if csv_column_name == '交易时间':
                field_value = parse_datetime(csv_value)
            elif csv_column_name == '收/支':
                field_value = parse_transaction_type(csv_value)
            elif csv_column_name == '金额(元)':
                transaction_type_str = row_dict.get('收/支')  # 获取 '收/支' 类型字符串
                transaction_type = parse_transaction_type(transaction_type_str)  # 解析交易类型
                field_value = parse_amount_yuan_wechat(csv_value, transaction_type)  # 使用微信金额解析函数

            bill_item[field_name] = field_value

         # 特殊处理 '备注' 字段 (微信账单中 '备注' 列本身就有值，这里不再额外生成备注，直接使用原始备注)
        bill_item['备注'] = bill_item.get('备注_原始', '').strip()  #  如果 '备注_原始' 列为空，则默认为空字符串

        transaction_type = bill_item.get('类型')
        if transaction_type != '不计收支':  #  微信账单中没有 "不计收支" 类型，这里可以移除这个判断，或者保留以兼容未来可能的 "不计收支" 交易类型
            bill_data.append(bill_item)

    return bill_data

# -------------------------------- 主解析函数 (微信账单) --------------------------------

def parse_wechat_csv_bill(csv_filepath):
    """
    解析微信 CSV 账单文件，提取账单信息。

    Args:
        csv_filepath (str): 微信账单 CSV 文件路径。

    Returns:
        list: 账单信息列表，每个元素为字典。
              如果解析过程中出现错误，返回 None。
    """
    try:
        with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header_row = None
            data_start = False
            for row in reader:
                if not data_start:
                    if row and row[0] == '交易时间' and row[1] == '交易类型':  #  通过检查表头行来判断数据开始
                        header_row = row
                        data_start = True
                        break
                    else:
                        continue  # 跳过非数据行 (文件头信息行)

            if not header_row:
                print("错误: 未找到账单数据表头行")
                return None

            bill_data = _parse_wechat_csv_data_rows(reader, header_row)
            return bill_data

    except FileNotFoundError:
        print(f"错误: 文件未找到: {csv_filepath}")
        return None
    except Exception as e:
        print(f"解析 CSV 文件出错: {e}")
        return None
