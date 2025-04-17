import asyncio
import os
import time
import pyautogui
from ui_tars_parser import UITarsParser
from ui_tars_executor import UITarsExecutor

# 简单的示例函数，解析和执行模型输出
def parse_and_execute_output(model_output):
    """
    解析和执行模型输出
    
    Args:
        model_output (str): 模型输出文本
        
    Returns:
        dict: 执行结果
    """
    # 初始化解析器和执行器
    parser = UITarsParser()
    executor = UITarsExecutor()
    
    # 解析输出
    parsed_result = parser.parse_output(model_output)
    
    print(f"思考内容:")
    print(parsed_result["thought"])
    print("\n动作:")
    print(f"类型: {parsed_result['action']['type']}")
    print(f"参数: {parsed_result['action']['params']}")
    
    # 执行动作
    print("\n准备执行动作...")
    time.sleep(2)  # 给用户时间准备
    
    # 执行动作并返回结果
    return executor.execute(parsed_result["action"])

# 主函数
async def main():
    # 示例1: 简单的点击操作
    print("=" * 50)
    print("示例1: 点击操作")
    print("=" * 50)
    
    click_output = """Thought: 我需要点击屏幕上的"开始"按钮，它位于屏幕左下角的位置。点击它可以打开开始菜单。
Action: click(start_box='[17, 980, 50, 990]')"""
    
    print("3秒后将执行点击操作...")
    time.sleep(3)
    result = parse_and_execute_output(click_output)
    print(f"执行结果: {result}")
    
    # 示例2: 键盘输入操作
    print("\n" + "=" * 50)
    print("示例2: 键盘输入操作")
    print("=" * 50)
    
    type_output = """Thought: 我需要在搜索框中输入"记事本"，这样可以搜索并找到记事本应用程序。
Action: type(content='记事本')"""
    
    print("3秒后将执行键盘输入操作...")
    time.sleep(3)
    result = parse_and_execute_output(type_output)
    print(f"执行结果: {result}")
    
    # 示例3: 热键操作
    print("\n" + "=" * 50)
    print("示例3: 热键操作")
    print("=" * 50)
    
    hotkey_output = """Thought: 我现在需要按下回车键来确认搜索。
Action: hotkey(key='enter')"""
    
    print("3秒后将执行热键操作...")
    time.sleep(3)
    result = parse_and_execute_output(hotkey_output)
    print(f"执行结果: {result}")
    
    # 测试完成
    print("\n所有示例执行完毕！")

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main()) 