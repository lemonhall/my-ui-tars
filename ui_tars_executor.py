import pyautogui
import time
import re
import logging
import pyperclip  # 添加剪贴板支持

class UITarsExecutor:
    """
    UI-TARS执行器类，实际执行UI-TARS模型输出的操作
    """
    
    def __init__(self, screen_width=None, screen_height=None):
        """
        初始化UI操作执行器
        
        Args:
            screen_width (int, optional): 屏幕宽度，默认自动获取
            screen_height (int, optional): 屏幕高度，默认自动获取
        """
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True  # 移动鼠标到屏幕角落将中止程序
        
        # 获取屏幕尺寸
        if screen_width and screen_height:
            self.screen_width = screen_width
            self.screen_height = screen_height
        else:
            self.screen_width, self.screen_height = pyautogui.size()
        
        # 初始化日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("UITarsExecutor")
    
    def execute(self, action_data):
        """
        执行UI操作
        
        Args:
            action_data (dict): 操作数据，包含type和params
            
        Returns:
            dict: 执行结果
        """
        if not action_data:
            return {"status": "error", "message": "没有可执行的动作"}
        
        action_type = action_data["type"]
        params = action_data["params"]
        
        self.logger.info(f"执行动作: {action_type}, 参数: {params}")
        
        try:
            # 根据动作类型分发到相应的处理方法
            if action_type == "click":
                return self._execute_click(params)
            elif action_type == "left_double":
                return self._execute_double_click(params)
            elif action_type == "right_single":
                return self._execute_right_click(params)
            elif action_type == "drag":
                return self._execute_drag(params)
            elif action_type == "hotkey":
                return self._execute_hotkey(params)
            elif action_type == "type":
                return self._execute_type(params)
            elif action_type == "scroll":
                return self._execute_scroll(params)
            elif action_type == "wait":
                return self._execute_wait(params)
            elif action_type == "finished":
                return self._execute_finished(params)
            else:
                return {"status": "error", "message": f"未知的动作类型: {action_type}"}
        except Exception as e:
            self.logger.error(f"执行动作异常: {str(e)}")
            return {"status": "error", "message": f"执行异常: {str(e)}"}
    
    def _parse_coordinates(self, coords_str):
        """
        解析坐标字符串
        
        Args:
            coords_str (str): 坐标字符串，如 "[123, 456, 789, 987]"
            
        Returns:
            list: 解析后的坐标
        """
        if not coords_str:
            return None
        
        # 查找所有数字
        coords = re.findall(r'\d+', coords_str)
        if not coords or len(coords) < 2:
            return None
        
        return [int(c) for c in coords]
    
    def _convert_to_absolute_coordinates(self, coords):
        """
        将模型输出的坐标转换为绝对坐标
        
        Args:
            coords (list): 相对坐标列表
            
        Returns:
            tuple or list: 绝对坐标，点击位置或区域
        """
        if not coords or len(coords) < 2:
            return None
        
        # 如果只有两个坐标（单点），转换为绝对坐标
        if len(coords) == 2:
            x = round(int(coords[0]) * self.screen_width / 1000)
            y = round(int(coords[1]) * self.screen_height / 1000)
            return (x, y)
        
        # 如果有四个坐标（矩形区域），转换为绝对坐标
        elif len(coords) == 4:
            x1 = round(int(coords[0]) * self.screen_width / 1000)
            y1 = round(int(coords[1]) * self.screen_height / 1000)
            x2 = round(int(coords[2]) * self.screen_width / 1000)
            y2 = round(int(coords[3]) * self.screen_height / 1000)
            
            # 计算中心点
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            return (center_x, center_y)
        
        return None
    
    def _execute_click(self, params):
        """
        执行点击操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        start_box = params.get("start_box")
        if not start_box:
            return {"status": "error", "message": "缺少start_box参数"}
        
        coords = self._parse_coordinates(start_box)
        abs_coords = self._convert_to_absolute_coordinates(coords)
        
        if not abs_coords:
            return {"status": "error", "message": "无法解析坐标"}
        
        x, y = abs_coords
        self.logger.info(f"点击位置: ({x}, {y})")
        pyautogui.click(x, y)
        
        return {
            "status": "success", 
            "message": f"点击操作成功执行，位置: ({x}, {y})",
            "coords": {"x": x, "y": y}
        }
    
    def _execute_double_click(self, params):
        """
        执行双击操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        start_box = params.get("start_box")
        if not start_box:
            return {"status": "error", "message": "缺少start_box参数"}
        
        coords = self._parse_coordinates(start_box)
        abs_coords = self._convert_to_absolute_coordinates(coords)
        
        if not abs_coords:
            return {"status": "error", "message": "无法解析坐标"}
        
        x, y = abs_coords
        self.logger.info(f"双击位置: ({x}, {y})")
        pyautogui.doubleClick(x, y)
        
        return {
            "status": "success", 
            "message": f"双击操作成功执行，位置: ({x}, {y})",
            "coords": {"x": x, "y": y}
        }
    
    def _execute_right_click(self, params):
        """
        执行右键点击操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        start_box = params.get("start_box")
        if not start_box:
            return {"status": "error", "message": "缺少start_box参数"}
        
        coords = self._parse_coordinates(start_box)
        abs_coords = self._convert_to_absolute_coordinates(coords)
        
        if not abs_coords:
            return {"status": "error", "message": "无法解析坐标"}
        
        x, y = abs_coords
        self.logger.info(f"右键点击位置: ({x}, {y})")
        pyautogui.rightClick(x, y)
        
        return {
            "status": "success", 
            "message": f"右键点击操作成功执行，位置: ({x}, {y})",
            "coords": {"x": x, "y": y}
        }
    
    def _execute_drag(self, params):
        """
        执行拖拽操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        start_box = params.get("start_box")
        end_box = params.get("end_box")
        
        if not start_box or not end_box:
            return {"status": "error", "message": "缺少start_box或end_box参数"}
        
        start_coords = self._parse_coordinates(start_box)
        end_coords = self._parse_coordinates(end_box)
        
        start_abs = self._convert_to_absolute_coordinates(start_coords)
        end_abs = self._convert_to_absolute_coordinates(end_coords)
        
        if not start_abs or not end_abs:
            return {"status": "error", "message": "无法解析坐标"}
        
        start_x, start_y = start_abs
        end_x, end_y = end_abs
        
        self.logger.info(f"拖拽: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
        
        # 移动到起始位置，按下鼠标，移动到结束位置，释放鼠标
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(end_x, end_y, duration=0.5)  # 使用duration参数使拖动平滑
        pyautogui.mouseUp()
        
        return {
            "status": "success", 
            "message": f"拖拽操作成功执行，从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})",
            "start": {"x": start_x, "y": start_y},
            "end": {"x": end_x, "y": end_y}
        }
    
    def _execute_hotkey(self, params):
        """
        执行热键操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        key = params.get("key")
        if not key:
            return {"status": "error", "message": "缺少key参数"}
        
        self.logger.info(f"执行热键: {key}")
        
        # 处理组合键
        keys = key.split()
        
        # 使用pyautogui的hotkey函数
        pyautogui.hotkey(*keys)
        
        return {
            "status": "success", 
            "message": f"热键操作成功执行: {key}"
        }
    
    def _execute_type(self, params):
        """
        执行键盘输入操作，使用剪贴板方式支持中文输入
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        content = params.get("content")
        if content is None:
            return {"status": "error", "message": "缺少content参数"}
        
        self.logger.info(f"键盘输入: {content}")
        
        # 添加短暂延迟，确保输入框已准备好接收输入
        time.sleep(0.5)
        
        # 检查是否需要在输入后按回车（如果内容以\n结尾）
        press_enter = False
        if content.endswith('\n'):
            content = content[:-1]  # 移除\n
            press_enter = True
        
        # 保存当前剪贴板内容
        try:
            original_clipboard = pyperclip.paste()
        except:
            original_clipboard = ""
        
        # 使用剪贴板方式输入文本（尤其适用于中文等非ASCII字符）
        try:
            # 复制内容到剪贴板
            pyperclip.copy(content)
            time.sleep(0.2)  # 短暂等待确保复制成功
            
            # 使用热键粘贴
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)  # 等待粘贴完成
            
            # 如果需要回车，按回车键
            if press_enter:
                time.sleep(0.2)  # 在按回车前稍作等待
                self.logger.info("按下回车键")
                pyautogui.press('enter')
            
            # 恢复原来的剪贴板内容
            pyperclip.copy(original_clipboard)
            
            # 完成后再等待一下，让系统有时间处理输入
            time.sleep(0.3)
            
            return {
                "status": "success", 
                "message": f"键盘输入操作成功执行，内容: {content}" + (" (已按回车)" if press_enter else "")
            }
        except Exception as e:
            # 恢复原来的剪贴板内容
            pyperclip.copy(original_clipboard)
            return {"status": "error", "message": f"键盘输入失败: {str(e)}"}
    
    def _execute_scroll(self, params):
        """
        执行滚动操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        start_box = params.get("start_box")
        direction = params.get("direction")
        
        if not start_box or not direction:
            return {"status": "error", "message": "缺少start_box或direction参数"}
        
        coords = self._parse_coordinates(start_box)
        abs_coords = self._convert_to_absolute_coordinates(coords)
        
        if not abs_coords:
            return {"status": "error", "message": "无法解析坐标"}
        
        x, y = abs_coords
        
        # 移动到位置
        pyautogui.moveTo(x, y)
        
        # 根据方向滚动
        clicks = 10  # 滚动距离
        
        if direction == "up":
            self.logger.info(f"向上滚动，位置: ({x}, {y})")
            pyautogui.scroll(clicks)
        elif direction == "down":
            self.logger.info(f"向下滚动，位置: ({x}, {y})")
            pyautogui.scroll(-clicks)
        elif direction == "left":
            self.logger.info(f"向左滚动，位置: ({x}, {y})")
            pyautogui.hscroll(-clicks)
        elif direction == "right":
            self.logger.info(f"向右滚动，位置: ({x}, {y})")
            pyautogui.hscroll(clicks)
        else:
            return {"status": "error", "message": f"未知的滚动方向: {direction}"}
        
        return {
            "status": "success", 
            "message": f"滚动操作成功执行，方向: {direction}, 位置: ({x}, {y})",
            "coords": {"x": x, "y": y},
            "direction": direction
        }
    
    def _execute_wait(self, params):
        """
        执行等待操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        self.logger.info("等待5秒")
        time.sleep(5)
        
        # 可以选择在这里截屏
        # screenshot = pyautogui.screenshot()
        # screenshot.save("wait_screenshot.png")
        
        return {
            "status": "success", 
            "message": "等待操作成功执行，等待5秒"
        }
    
    def _execute_finished(self, params):
        """
        执行完成操作
        
        Args:
            params (dict): 操作参数
            
        Returns:
            dict: 执行结果
        """
        content = params.get("content", "")
        self.logger.info(f"任务完成: {content}")
        
        return {
            "status": "success", 
            "message": f"任务标记为完成，内容: {content}",
            "content": content
        }


# 测试代码
if __name__ == "__main__":
    # 初始化执行器
    executor = UITarsExecutor()
    
    # 测试点击操作
    click_action = {
        "type": "click",
        "params": {
            "start_box": "[500, 500, 550, 550]"
        }
    }
    
    # 睡眠3秒，给用户时间切换到合适的窗口
    print("3秒后将在屏幕中心附近执行点击操作...")
    time.sleep(3)
    
    # 执行点击
    result = executor.execute(click_action)
    print(f"执行结果: {result}")
    
    # 测试键盘输入
    type_action = {
        "type": "type",
        "params": {
            "content": "这是一个测试"
        }
    }
    
    # 执行输入
    print("现在将执行键盘输入...")
    result = executor.execute(type_action)
    print(f"执行结果: {result}")
    
    # 测试热键操作
    hotkey_action = {
        "type": "hotkey",
        "params": {
            "key": "ctrl a"
        }
    }
    
    # 执行热键
    print("现在将执行Ctrl+A热键操作...")
    result = executor.execute(hotkey_action)
    print(f"执行结果: {result}")
    
    # 完成测试
    print("测试完成！") 