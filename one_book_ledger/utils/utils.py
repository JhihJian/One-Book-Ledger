# -*- coding: utf-8 -*-
"""
通用工具函数模块
"""
import datetime
import logging
import re
import openpyxl
import csv
from enum import Enum # 导入 Enum

# -------------------------------- 交易类型枚举 ---------------------------------
class TransactionType(Enum):
    """交易类型枚举"""
    UNKNOWN = "未知类型"
    PAYMENT = "支付"
    TRANSFER = "转账"
    RECHARGE = "充值"
    REFUND = "退款"
    WITHDRAWAL = "提现"
    DINING = "餐饮美食"
    TRANSPORTATION = "交通出行"
    SHOPPING = "购物消费"
    ENTERTAINMENT = "休闲娱乐"
    DAILY_NECESSITIES = "日用百货"
    SUPERMARKET = "商超购物"
    GROCERY = "生鲜食品"
    DIGITAL_PRODUCTS = "数码家电"
    CLOTHING = "服饰鞋包"
    BEAUTY_COSMETICS = "美妆个护"
    BOOKS_MEDIA = "图书音像"
    TRAVEL = "旅游出行"
    HOUSING = "住房缴费"
    UTILITIES = "水电煤缴费"
    TELECOMMUNICATIONS = "通讯缴费"
    FINANCIAL_SERVICES = "金融服务"
    SALARY = "工资收入"
    INVESTMENT_INCOME = "投资理财"
    INTEREST = "利息收入"
    TAX_REFUND = "退税"
    CREDIT_CARD_REPAYMENT = "信用卡还款"
    CASH_WITHDRAWAL = "现金提取"
    OTHERS = "其他"


# -------------------------------- 标准化交易类型函数 ---------------------------------
def standardize_transaction_type(transaction_summary):
    """
    标准化交易摘要为统一的交易类型.

    Args:
        transaction_summary (str): 交易摘要字符串.

    Returns:
        str: 标准化后的交易类型 (TransactionType 枚举值).
    """
    summary = transaction_summary.lower() #  转换为小写，方便匹配

    # 餐饮美食
    if re.search(r'^(麦当劳|肯德基|星巴克|咖啡|餐饮|美食|茶饮|小吃|快餐|外卖|餐厅|饭店|食堂|自助餐|火锅|烧烤|烤肉|披萨|汉堡|炸鸡|奶茶|果汁|面包|蛋糕|甜点|零食|夜宵|早点|午餐|晚餐|宵夜|下午茶|咖啡馆|餐馆|小馆|饭馆|酒楼|菜馆|茶餐厅|料理|美食城| food | eat | dining | restaurant | coffee | cafe | mcdonald\'s | kfc | starbucks)', summary):
        return TransactionType.DINING.value

    # 交通出行
    elif re.search(r'^(地铁|公交|滴滴|打车|出租车|共享单车|单车|自行车|火车|高铁|机票| bus | subway | taxi | ride | bike | transportation | travel | airport | railway | station | 轨道交通)', summary):
        return TransactionType.TRANSPORTATION.value

    # 购物消费 (更细化的购物类型可以继续添加)
    elif re.search(r'^(淘宝|天猫|京东|拼多多|亚马逊|当当|唯品会|苏宁易购|国美电器|超市|商场|购物|消费|买| purchase | shop | shopping | tmall | taobao | jd.com | pdd | amazon | supermarket | mall | store | 门店|便利店|7-eleven|全家|屈臣氏|沃尔玛|家乐福|华联|物美|永辉|京客隆|超市发|超市发超市)', summary):
        return TransactionType.SHOPPING.value

    # 休闲娱乐
    elif re.search(r'^(电影|KTV|酒吧|剧院|演出|展览|演唱会|音乐会|体育赛事|健身|运动|游戏|视频会员|音乐会员|电影票|ktv | bar | theater | performance | exhibition | concert | sports | fitness | exercise | game | movie | entertainment | leisure)', summary):
        return TransactionType.ENTERTAINMENT.value

    # 日用百货
    elif re.search(r'^(日用品|百货|家居|家纺|厨具|餐具|家电|电器|数码|手机|电脑|办公用品|文具|纸巾|牙膏|洗发水|沐浴露|洗衣液|卫生巾| household | daily use | necessities | home | furniture | appliance | digital | stationery | paper | tissue | toothpaste | shampoo | body wash | laundry detergent)', summary):
        return TransactionType.DAILY_NECESSITIES.value

    # 商超购物 (可以更精细化)
    elif re.search(r'^(超市|商场|shopping mall|supermarket|mart|grocery store| hypermarket)', summary):
        return TransactionType.SUPERMARKET.value

    # 生鲜食品
    elif re.search(r'^(生鲜|水果|蔬菜|肉|禽|蛋|海鲜|水产| dairy | fruit | vegetable | meat | seafood | grocery | produce | fresh food)', summary):
        return TransactionType.GROCERY.value

    # 数码家电
    elif re.search(r'^(数码产品|电子产品|家电|手机|电脑|平板|相机|电视|冰箱|洗衣机|空调| digital product | electronics | appliance | mobile phone | computer | tablet | camera | tv | refrigerator | washing machine | air conditioner)', summary):
        return TransactionType.DIGITAL_PRODUCTS.value

     # 服饰鞋包
    elif re.search(r'^(服装|衣服|鞋子|包|帽子|围巾|手套| fashion | clothing | clothes | shoes | bags | hats | scarves | gloves)', summary):
        return TransactionType.CLOTHING.value

    # 美妆个护
    elif re.search(r'^(化妆品|护肤品|彩妆|香水| personal care | beauty | cosmetics | makeup | perfume | skincare | 美容|个护)', summary):
        return TransactionType.BEAUTY_COSMETICS.value

    # 图书音像
    elif re.search(r'^(图书|书籍|书店|音像制品|电影|音乐|唱片|书本|杂志|报纸|电子书| ebook | books | bookstore | media | film | music | cd | magazine | newspaper)', summary):
        return TransactionType.BOOKS_MEDIA.value

    # 旅行
    elif re.search(r'^(旅行|酒店|住宿|景点|机票|火车票|旅游|旅馆|客栈|酒店住宿|hotel | accommodation | scenic spot | flight ticket | train ticket | travel | tourism | hostel | inn)', summary):
        return TransactionType.TRAVEL.value

    # 住房缴费
    elif re.search(r'^(房租|物业费|房贷|租房| mortgage | rent | property management fee | housing payment)', summary):
        return TransactionType.HOUSING.value

    # 水电煤缴费
    elif re.search(r'^(水费|电费|燃气费| energy bill | water bill | electricity bill | gas bill | utility bill | 水电费|煤气费)', summary):
        return TransactionType.UTILITIES.value

    # 通讯缴费
    elif re.search(r'^(话费|流量费|宽带费|网费|通讯费|电话费|手机费|通信费| telecommunication fee | phone bill | mobile bill | internet fee | broadband fee | network fee)', summary):
        return TransactionType.TELECOMMUNICATIONS.value

    # 金融服务 (可以更精细化)
    elif re.search(r'^(理财|保险|证券|基金|股票|期货|银行|支付|贷款| finance | insurance | securities | fund | stock | futures | bank | payment | loan | 金融|理财产品| investment)', summary):
        return TransactionType.FINANCIAL_SERVICES.value

    # 工资收入
    elif re.search(r'^(工资|薪资| salary | wage | income | 收入-工资)', summary): # "收入-工资" 匹配 微信账单中的 "收入-工资" 类型
        return TransactionType.SALARY.value

    # 投资理财收入
    elif re.search(r'^(投资收入|理财收入|分红| dividend | investment income | wealth management income)', summary):
        return TransactionType.INVESTMENT_INCOME.value

    # 利息收入
    elif re.search(r'^(利息| interest | 收益-利息)', summary): # "收益-利息" 匹配 微信账单中的 "收益-利息" 类型
        return TransactionType.INTEREST.value

    # 退税
    elif re.search(r'^(退税| tax refund )', summary):
        return TransactionType.TAX_REFUND.value

    # 信用卡还款
    elif re.search(r'^(信用卡还款| credit card repayment )', summary):
        return TransactionType.CREDIT_CARD_REPAYMENT.value

    # 现金提取/提现
    elif re.search(r'^(现金提取|提现| withdraw | cash withdrawal )', summary):
        return TransactionType.CASH_WITHDRAWAL.value

    # 支付 (更通用的支付类型，放在最后匹配)
    elif re.search(r'^(支付|付款|缴费| spend | pay | payment | expense)', summary):
        return TransactionType.PAYMENT.value

    # 转账
    elif re.search(r'^(转账| transfer | 支出-转账)', summary): # "支出-转账" 匹配 微信账单中的 "支出-转账" 类型
        return TransactionType.TRANSFER.value

    # 充值
    elif re.search(r'^(充值| recharge | 收入-充值)', summary): # "收入-充值" 匹配 微信账单中的 "收入-充值" 类型
        return TransactionType.RECHARGE.value

    # 退款
    elif re.search(r'^(退款| refund )', summary):
        return TransactionType.REFUND.value

    return TransactionType.UNKNOWN.value # 默认未知类型


# -------------------------------- 金额解析函数 ---------------------------------
def parse_amount(amount_str, transaction_type=TransactionType.UNKNOWN): #  添加 transaction_type 参数，并设置默认值为 UNKNOWN
    """
    解析金额字符串为浮点数.

    Args:
        amount_str (str): 金额字符串.
        transaction_type (TransactionType, optional): 交易类型 (用于更精细化的金额解析). 默认为 TransactionType.UNKNOWN.

    Returns:
        float: 解析后的金额 (浮点数).
             如果解析失败，则返回 0.0，并在控制台输出警告信息。
    """
    try:
        #  尝试直接将字符串转换为 float
        amount = float(amount_str)
        return amount
    except ValueError:
        try:
            #  处理千分位分隔符 (例如 "1,234.56")
            amount = float(amount_str.replace(',', ''))
            return amount
        except ValueError:
            try:
                #  处理中文金额格式 (例如 "￥123.45" 或 "CNY 123.45")
                amount_match = re.search(r'[\uFFE5¥\$](-?[\d,\.]+(?:\.\d{2})?)', amount_str) # 匹配人民币/日元/美元符号及金额
                if amount_match:
                    amount_value = amount_match.group(1).replace(',', '')
                    return float(amount_value)
                else:
                    amount_match_cny_prefix = re.search(r'CNY\s*(-?[\d,\.]+(?:\.\d{2})?)', amount_str, re.IGNORECASE) # 匹配 "CNY" 前缀
                    if amount_match_cny_prefix:
                        amount_value = amount_match_cny_prefix.group(1).replace(',', '')
                        return float(amount_value)
                    else:
                        raise ValueError # 抛出 ValueError，进入 except 块统一处理
            except ValueError:
                logging.warning(f"警告: 金额解析失败: {amount_str}, 交易类型: {transaction_type.value}") # 包含交易类型信息
                return 0.0 # 解析失败返回 0.0


# -------------------------------- 日期时间解析函数 ---------------------------------
def parse_datetime(datetime_value, date_format=None):
    """
    解析日期时间字符串为 datetime 对象.
    ...
    """
    if not datetime_value:
        return None #  如果值为空，直接返回 None

    if isinstance(datetime_value, datetime.datetime):
        return datetime_value # 如果已经是 datetime 对象，直接返回

    if date_format:
        try:
            return datetime.datetime.strptime(datetime_value, date_format)
        except ValueError as e: ###  添加调试日志  ###
            logging.warning(f"警告: 日期时间解析失败 (指定格式): {datetime_value}, 格式: {date_format}, 错误信息: {e}") ###  添加调试日志，输出具体错误信息 ###
            return None
    else:
        # 尝试自动推断常见格式 (根据实际账单格式添加更多格式)
        formats_to_try = [
            '%Y-%m-%d %H:%M:%S', #  常见格式 1:  例如 '2023-10-26 10:30:00'
            # ... (其他格式字符串) ...
        ]
        for fmt in formats_to_try:
            try:
                return datetime.datetime.strptime(datetime_value, fmt)
            except ValueError as e: ###  添加调试日志  ###
                logging.debug(f"尝试格式 '{fmt}' 解析日期 '{datetime_value}' 失败: {e}") ###  添加调试日志，输出尝试的格式和错误信息 ###
                continue # 尝试下一个格式

        logging.warning(f"警告: 日期时间解析失败 (自动推断格式): {datetime_value}, 尝试格式: {formats_to_try}")
        return None # 所有格式都尝试失败后返回 None

# -------------------------------- XLS 账单文件解析函数 ---------------------------------

def parse_xls_bill(xls_filepath, column_name_mapping):
    """
    通用 XLS 账单文件解析函数.

    Args:
        xls_filepath (str): XLS 账单文件路径.
        column_name_mapping (dict): XLS 列名到通用字段名的映射字典.
                                        例如: {'交易日期': '日期', '交易摘要': '交易摘要', ...}

    Returns:
        list: 账单信息列表，每个元素为字典。
              如果解析过程中出现错误，返回 None.
    """
    bill_data = []
    try:
        workbook = openpyxl.load_workbook(xls_filepath)
        sheet = workbook.active
        header_row = [cell.value for cell in sheet[1]] # 获取表头行

        if not header_row:
            logging.error(f"错误: XLS 文件缺少表头行: {xls_filepath}") # 使用 logging 输出错误
            return None

        # 获取列索引
        column_indices = {}
        for col_name_xls, field_name in column_name_mapping.items():
            try:
                column_indices[field_name] = header_row.index(col_name_xls)
            except ValueError:
                logging.warning(f"警告: XLS 文件缺少列: {col_name_xls}") # 使用 logging 输出警告
                column_indices[field_name] = None #  如果找不到列，则设置为 None

        # 从第二行开始遍历数据行
        for row_index in range(2, sheet.max_row + 1):
            bill_item = {}
            row_values = [cell.value for cell in sheet[row_index]]

            if not any(row_values): # 跳过空行
                continue

            try:
                for field_name, col_index in column_indices.items():
                    if col_index is not None: #  只处理找到的列
                        bill_item[field_name] = row_values[col_index]
                bill_data.append(bill_item)

            except Exception as e:
                logging.warning(f"解析 XLS 账单行出错 (行号: {row_index}): {e}") # 使用 logging 输出警告，包含行号
                continue # 跳过错误行

        return bill_data

    except FileNotFoundError:
        logging.error(f"错误: 文件未找到: {xls_filepath}") # 使用 logging 输出错误
        return None
    except Exception as e:
        logging.error(f"解析 XLS 文件出错: {e}") # 使用 logging 输出错误
        return None