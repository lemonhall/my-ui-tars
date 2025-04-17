import sys
import os
import time

# 添加项目根目录到Python路径，确保能导入ui_tars_executor模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui_tars_executor import UITarsExecutor

def test_type_function():
    """测试UITarsExecutor的键盘输入功能"""
    # 初始化执行器
    executor = UITarsExecutor()
    
    print("请在5秒内打开一个文本编辑器并将光标放在可输入的位置...")
    time.sleep(5)
    
    # 测试简单输入
    simple_test = {
        "type": "type",
        "params": {
            "content": "测试简单中文输入"
        }
    }
    
    print("测试简单中文输入...")
    result = executor.execute(simple_test)
    print(f"执行结果: {result}")
    time.sleep(2)
    
    # 测试带换行的输入
    newline_test = {
        "type": "type",
        "params": {
            "content": "测试带换行的输入\n"
        }
    }
    
    print("测试带换行的输入...")
    result = executor.execute(newline_test)
    print(f"执行结果: {result}")
    time.sleep(2)
    
    # 测试长文本输入
    long_test = {
        "type": "type",
        "params": {
            "content": "这是一段较长的测试文本，包含了中文、数字123和英文ABC，测试多种字符的输入情况。"
        }
    }
    
    print("测试长文本输入...")
    result = executor.execute(long_test)
    print(f"执行结果: {result}")
    
    print("测试完成!")

if __name__ == "__main__":
    test_type_function() 