import os

def create_project_structure(project_dir):
    """
    自动创建 One-Book-Ledger 项目目录结构.

    Args:
        project_dir (str): 项目根目录路径.
    """

    # 目录结构定义
    dirs = [
        os.path.join(project_dir, '../one_book_ledger2'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser'),
        os.path.join(project_dir, '../one_book_ledger2', 'ledger_manager'),
        os.path.join(project_dir, '../one_book_ledger2', 'gui'),
        os.path.join(project_dir, '../one_book_ledger2', 'utils'),
        os.path.join(project_dir, 'tests'),
        os.path.join(project_dir, 'tests', 'test_bill_parser'),
        os.path.join(project_dir, 'tests', 'test_ledger_manager'),
        os.path.join(project_dir, 'docs'),
        os.path.join(project_dir, 'resources'),
        os.path.join(project_dir, 'resources', 'icons'),
        os.path.join(project_dir, 'resources', 'ui'),
        os.path.join(project_dir, 'build'),
        os.path.join(project_dir, 'dist'),
    ]

    # 文件定义 (空文件)
    files = [
        os.path.join(project_dir, '../one_book_ledger2', '__init__.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser', '__init__.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser', 'alipay_parser.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser', 'wechat_parser.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser', 'citic_parser.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser', 'pufa_parser.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'bill_parser', 'jdbt_parser.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'ledger_manager', '__init__.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'ledger_manager', 'ledger.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'ledger_manager', 'data_exporter.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'gui', '__init__.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'gui', 'main_window.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'gui', 'bill_import_dialog.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'gui', 'ledger_view.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'utils', '__init__.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'utils', 'file_utils.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'utils', 'config_utils.py'),
        os.path.join(project_dir, '../one_book_ledger2', 'main.py'),
        os.path.join(project_dir, 'tests', '__init__.py'),
        os.path.join(project_dir, 'tests', 'test_bill_parser', '__init__.py'),
        os.path.join(project_dir, 'tests', 'test_bill_parser', 'test_alipay_parser.py'),
        os.path.join(project_dir, 'tests', 'test_ledger_manager', '__init__.py'),
        os.path.join(project_dir, 'tests', 'test_ledger_manager', 'test_ledger.py'),
        os.path.join(project_dir, 'docs', '.gitkeep'), # 文档目录可以放一个 .gitkeep 占位文件，或者其他文档文件
        os.path.join(project_dir, 'resources', 'icons', '.gitkeep'), # 资源目录下的子目录也放 .gitkeep
        os.path.join(project_dir, 'resources', 'ui', '.gitkeep'),
        os.path.join(project_dir, 'build', '.gitkeep'),
        os.path.join(project_dir, 'dist', '.gitkeep'),
        os.path.join(project_dir, 'LICENSE'),
        os.path.join(project_dir, 'requirements.txt'),
        os.path.join(project_dir, 'setup.py'),
        os.path.join(project_dir, '.gitignore'),
    ]

    # 创建目录
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True) # exist_ok=True 表示如果目录已存在，不会报错

    # 创建空文件
    for file_path in files:
        if not os.path.exists(file_path): # 避免覆盖已存在的文件 (例如 LICENSE, README.md)
            with open(file_path, 'w') as f:
                pass # 创建空文件

    print(f"项目目录结构已成功创建在: {project_dir}")

if __name__ == "__main__":
    project_root_dir = '../one_book_ledger2'  # 设置项目根目录名称
    create_project_structure(project_root_dir)