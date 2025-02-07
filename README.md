# One-Book-Ledger

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![GitHub Stars](https://img.shields.io/github/stars/your-username/One-Book-Ledger)](https://github.com/your-username/One-Book-Ledger/stargazers)  
[![GitHub Issues](https://img.shields.io/github/issues/your-username/One-Book-Ledger)](https://github.com/your-username/One-Book-Ledger/issues)

## 简介

One-Book-Ledger 是一款小而美的开源个人财务管理工具，专注整合多来源账单。它能将微信、支付宝、银行信用卡（中信、浦发）、京东白条账单导入并汇总到一本账簿，让财务状况一目了然。

## 核心功能

* **多平台账单导入：** 支持微信、支付宝、中信银行信用卡、浦发银行信用卡、京东白条账单。
* **历史账单文件管理：** 设定账单存放文件夹，对存放其中的账单文件进行管理
* **统一账簿管理：** 将多来源账单整合为一本账簿，方便查看和管理。
* **钱迹格式导出：** 支持导出为钱迹兼容的 Excel 格式。





| 支付宝账单字段 (CSV) | 微信账单字段 (待定) | 中信银行账单字段 (待定) | 浦发银行账单字段 (待定) | 统一账本账单字段 | |---|---|---|---|---| | 交易时间 |  |  |  | 交易日期 (datetime) | | (固定值: '支付宝') |  |  |  | 账户 (str) | | 商品名称 (主要), 交易类型/交易对方 (辅助) |  |  |  | 交易摘要 (str) | | 交易对方 (主要), 商品名称 (辅助) |  |  |  | 交易商户 (str) | | 金额 |  |  |  | 金额 (float) | | 备注 |  |  |  | 备注 (str) | | 交易类型 (用于标准化) |  |  |  | 交易类型 (str) |

## 安装

1. **克隆仓库：**
   ```bash
   git clone [https://github.com/your-username/One-Book-Ledger.git](https://www.google.com/search?q=https://github.com/your-username/One-Book-Ledger.git)
