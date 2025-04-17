import pyautogui
import time
import pyperclip  # 用于剪贴板操作，可能需要安装: pip install pyperclip

def test_direct_typing():
    """测试直接使用pyautogui.write输入中文"""
    print("3秒后将尝试直接输入中文...")
    time.sleep(3)
    
    text = "这是一个测试"
    print(f"尝试输入: {text}")
    pyautogui.write(text, interval=0.1)
    print("直接输入完成")

def test_clipboard_typing():
    """使用剪贴板方式输入中文"""
    print("3秒后将尝试通过剪贴板输入中文...")
    time.sleep(3)
    
    text = "这是一个测试"
    print(f"尝试通过剪贴板输入: {text}")
    
    # 保存当前剪贴板内容
    original = pyperclip.paste()
    
    # 复制要输入的文本到剪贴板
    pyperclip.copy(text)
    
    # 使用Ctrl+V粘贴
    pyautogui.hotkey('ctrl', 'v')
    
    # 恢复原来的剪贴板内容
    pyperclip.copy(original)
    
    print("剪贴板输入完成")

def test_key_by_key():
    """测试逐个字符输入"""
    print("3秒后将尝试逐个字符输入...")
    time.sleep(3)
    
    print("尝试按键盘上的A、B、C和数字1、2、3")
    for key in ['a', 'b', 'c', '1', '2', '3']:
        pyautogui.press(key)
        time.sleep(0.5)
    
    print("逐个字符输入完成")

if __name__ == "__main__":
    print("请打开一个文本编辑器并将光标放在可输入的位置")
    
    # 测试直接输入
    test_direct_typing()
    time.sleep(2)
    
    # 测试通过剪贴板输入
    test_clipboard_typing()
    time.sleep(2)
    
    # 测试逐个字符输入
    test_key_by_key()
    
    print("测试完成!") 