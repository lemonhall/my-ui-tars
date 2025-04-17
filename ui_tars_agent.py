from ui_tars_parser import UITarsParser
from agno.agent import Agent, RunResponse
from agno.models.deepseek import DeepSeek
from agno.media import Image
from ui_tars_executor import UITarsExecutor
import os
import time
import pyautogui
import json
import re

class UITarsAgent:
    """
    UI-TARS代理类，用于集成Agno框架和UI-TARS模型解析器
    """
    
    def __init__(self, model_id=None, base_url=None):
        """
        初始化UI-TARS代理
        
        Args:
            model_id (str, optional): 模型ID
            base_url (str, optional): API基础URL
        """
        # 默认使用README中提到的模型ID和URL
        self.model_id = model_id or "ep-20250417103958-d888s"  # TARS模型ID
        self.base_url = base_url or "https://ark.cn-beijing.volces.com/api/v3/"
        
        # 获取API密钥
        self.api_key = os.environ.get("HUOSHAN_API_KEY")
        if not self.api_key:
            raise ValueError("未设置HUOSHAN_API_KEY环境变量，请先设置API密钥")
            
        # 初始化解析器
        self.parser = UITarsParser()
        
        # 初始化执行器
        self.executor = UITarsExecutor()
        
        # 初始化Agno模型和代理
        self.model = DeepSeek(
            id=self.model_id,
            base_url=self.base_url,
            temperature=0,
            top_p=0.7
        )
        
        # 创建代理实例
        self.agent = Agent(
            model=self.model,
            name="我的UI助手",
            description="基于UI-TARS的自动化UI操作助手",
            instructions=self._get_instructions(),
            debug_mode=True,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
        )
    
    def _get_instructions(self):
        """
        获取代理指令
        """
        return """
You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task.
## Output Format
```
Thought: ...
Action: ...
```
## Action Space
click(start_box='[x1, y1, x2, y2]')
left_double(start_box='[x1, y1, x2, y2]')
right_single(start_box='[x1, y1, x2, y2]')
drag(start_box='[x1, y1, x2, y2]', end_box='[x3, y3, x4, y4]')
hotkey(key='')
type(content='') #If you want to submit your input, use "\\n" at the end of `content`.
scroll(start_box='[x1, y1, x2, y2]', direction='down or up or right or left')
wait() #Sleep for 5s and take a screenshot to check for any changes.
finished(content='xxx') # Use escape characters \\', \\", and \\n in content part to ensure we can parse the content in normal python string format.
## Note
- Use Chinese in `Thought` part.
- Write a small plan and finally summarize your next action (with its target element) in one sentence in `Thought` part.
## User Instruction
        """
    
    def process_task(self, task, screenshot_path=None):
        """
        处理UI任务
        
        Args:
            task (str): 用户任务描述
            screenshot_path (str, optional): 屏幕截图路径
            
        Returns:
            dict: 处理结果
        """
        # 准备图片参数（如果有）
        images = None
        if screenshot_path:
            # 创建本地图片对象
            images = [Image(filepath=screenshot_path)]
        
        # 调用Agno代理运行任务
        response = self.agent.run(task, images=images)
        
        # 解析模型输出
        parsed_result = self.parser.parse_output(response.content)
        
        # 执行动作
        execution_result = self._execute_ui_action(parsed_result["action"])
        
        return {
            "thought": parsed_result["thought"],
            "action": parsed_result["action"],
            "execution": execution_result,
            "raw_response": response.content
        }
    
    def _execute_ui_action(self, action_data):
        """
        执行UI动作
        
        Args:
            action_data (dict): 解析后的动作数据
            
        Returns:
            dict: 执行结果
        """
        if not action_data:
            return {"status": "error", "message": "没有可执行的动作"}
        
        # 调用执行器执行实际UI操作
        return self.executor.execute(action_data)


# 测试代码
if __name__ == "__main__":
    print("初始化UI-TARS代理...")
    agent = UITarsAgent()
    
    # 简单测试
    task = "点击发送按钮"
    
    print(f"处理任务: {task}")
    
    # 是否使用截图
    use_screenshot = True  # 设置为True启用截图
    screenshot_path = None
    
    if use_screenshot:
        try:
            screenshot_path = "current_screen.png"
            print(f"正在截取当前屏幕...")
            pyautogui.screenshot(screenshot_path)
            print(f"屏幕截图已保存至: {screenshot_path}")
        except Exception as e:
            print(f"截图失败: {e}")
            use_screenshot = False
            screenshot_path = None
    
    # 处理任务
    result = agent.process_task(task, screenshot_path)
    
    print(f"模型思考: {result['thought']}")
    print(f"解析的动作: {json.dumps(result['action'], ensure_ascii=False)}")
    print(f"执行结果: {json.dumps(result['execution'], ensure_ascii=False)}") 