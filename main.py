import asyncio
import json
import os
import time
import pyautogui
from ui_tars_parser import UITarsParser
from ui_tars_executor import UITarsExecutor
from agno.agent import Agent, RunResponse
from agno.models.deepseek import DeepSeek

class UITarsMain:
    """
    UI-TARS主程序，整合解析器、执行器和Agno代理
    """
    
    def __init__(self, model_id=None, base_url=None):
        """
        初始化UI-TARS主程序
        
        Args:
            model_id (str, optional): 模型ID
            base_url (str, optional): API基础URL
        """
        # 打印欢迎信息
        print("=" * 50)
        print("欢迎使用UI-TARS自动化助手")
        print("基于Agno框架和UI-TARS模型")
        print("=" * 50)
        
        # 检查API密钥
        self.api_key = os.environ.get("HUOSHAN_API_KEY")
        if not self.api_key:
            raise ValueError("未设置HUOSHAN_API_KEY环境变量，请先设置API密钥")
        
        # 默认使用README中提到的模型ID和URL
        self.model_id = model_id or "ep-20250417103958-d888s"  # TARS模型ID
        self.base_url = base_url or "https://ark.cn-beijing.volces.com/api/v3/"
        
        # 初始化解析器
        self.parser = UITarsParser()
        
        # 初始化执行器
        self.executor = UITarsExecutor()
        
        # 初始化Agno模型和代理
        print("初始化Agno模型和代理...")
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
        
        print("初始化完成！")
    
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
    
    async def run_task(self, task, use_screenshot=True, screenshot_path=None):
        """
        运行单个UI任务
        
        Args:
            task (str): 用户任务描述
            use_screenshot (bool): 是否使用屏幕截图
            screenshot_path (str, optional): 屏幕截图路径，如果为None则自动截图
            
        Returns:
            dict: 任务执行结果
        """
        # 准备任务上下文
        context = {
            "text": task
        }
        
        # 如果需要使用截图
        if use_screenshot:
            # 如果没有提供截图路径，则自动截图
            if not screenshot_path:
                screenshot_path = "current_screen.png"
                print(f"正在截取屏幕...")
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)
                print(f"屏幕截图已保存到: {screenshot_path}")
            
            # 添加截图到上下文
            context["files"] = [{"path": screenshot_path}]
        
        # 调用Agno代理运行任务
        print(f"正在处理任务: {task}")
        response = await self.agent.run(context)
        
        # 解析模型输出
        print("正在解析模型输出...")
        parsed_result = self.parser.parse_output(response.content)
        
        # 打印思考内容
        print(f"\n模型思考:")
        print(f"{parsed_result['thought']}\n")
        
        # 打印动作内容
        print(f"解析的动作:")
        print(json.dumps(parsed_result["action"], ensure_ascii=False, indent=2))
        
        # 执行动作
        if parsed_result["action"]:
            print("\n正在执行动作...")
            execution_result = self.executor.execute(parsed_result["action"])
            print(f"执行结果: {json.dumps(execution_result, ensure_ascii=False, indent=2)}")
        else:
            execution_result = {"status": "error", "message": "没有可执行的动作"}
            print(f"执行结果: {json.dumps(execution_result, ensure_ascii=False, indent=2)}")
        
        return {
            "thought": parsed_result["thought"],
            "action": parsed_result["action"],
            "execution": execution_result,
            "raw_response": response.content
        }
    
    async def run_interactive(self):
        """
        交互式运行UI-TARS助手
        """
        print("\n开始交互式会话，输入'退出'或'exit'结束会话\n")
        
        while True:
            # 获取用户任务
            task = input("\n请输入任务描述 (输入'退出'或'exit'结束): ")
            
            # 检查是否退出
            if task.lower() in ["退出", "exit", "quit", "q"]:
                print("会话结束，谢谢使用！")
                break
            
            # 询问是否使用截图
            use_screenshot = input("是否使用屏幕截图? (y/n): ").lower() == 'y'
            screenshot_path = None
            
            if use_screenshot:
                # 询问是否自动截图
                auto_screenshot = input("是否自动截图? (y/n): ").lower() == 'y'
                
                if not auto_screenshot:
                    screenshot_path = input("请输入截图路径: ")
                
                # 倒计时，给用户时间准备
                print("3秒后开始处理...")
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
            
            try:
                # 执行任务
                result = await self.run_task(task, use_screenshot, screenshot_path)
                
                # 打印简要结果
                if result["action"] and result["action"]["type"] == "finished":
                    print("\n任务已完成！")
                    if "content" in result["execution"]:
                        print(f"完成信息: {result['execution']['content']}")
                
            except Exception as e:
                print(f"执行任务时发生错误: {str(e)}")


# 主程序入口
if __name__ == "__main__":
    async def main():
        try:
            # 初始化UI-TARS主程序
            ui_tars = UITarsMain()
            
            # 运行交互式会话
            await ui_tars.run_interactive()
            
        except ValueError as e:
            print(f"错误: {str(e)}")
        except Exception as e:
            print(f"未预期的错误: {str(e)}")
    
    # 运行主函数
    asyncio.run(main()) 