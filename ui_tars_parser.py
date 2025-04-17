import re
import json

class UITarsParser:
    """
    解析UI-TARS模型输出的工具类，将模型动作转换为可执行的工具调用
    """
    
    def __init__(self):
        # 支持的动作类型及其参数
        self.action_types = {
            "click": ["start_box"],
            "left_double": ["start_box"],
            "right_single": ["start_box"],
            "drag": ["start_box", "end_box"],
            "hotkey": ["key"],
            "type": ["content"],
            "scroll": ["start_box", "direction"],
            "wait": [],
            "finished": ["content"]
        }
    
    def parse_output(self, model_output):
        """
        解析模型输出，提取思考和动作部分
        
        Args:
            model_output (str): 模型的原始输出文本
            
        Returns:
            dict: 包含thought和action的字典
        """
        # 分离Thought和Action部分
        thought_pattern = r"Thought: (.*?)(?:\nAction: |$)"
        action_pattern = r"Action: (.*?)$"
        
        thought_match = re.search(thought_pattern, model_output, re.DOTALL)
        action_match = re.search(action_pattern, model_output, re.DOTALL)
        
        thought = thought_match.group(1).strip() if thought_match else ""
        action_str = action_match.group(1).strip() if action_match else ""
        
        # 解析动作
        action_data = self.parse_action(action_str) if action_str else None
        
        return {
            "thought": thought,
            "action": action_data
        }
    
    def parse_action(self, action_str):
        """
        解析动作字符串为结构化数据
        
        Args:
            action_str (str): 动作字符串，如 "click(start_box='[10, 20, 30, 40]')"
            
        Returns:
            dict: 包含动作类型和参数的字典
        """
        # 提取动作类型和参数字符串
        action_match = re.match(r"(\w+)\((.*)\)", action_str)
        if not action_match:
            return None
        
        action_type = action_match.group(1)
        params_str = action_match.group(2)
        
        # 检查动作类型是否支持
        if action_type not in self.action_types:
            return {
                "type": "unknown",
                "raw": action_str
            }
        
        # 解析参数
        params = {}
        expected_params = self.action_types[action_type]
        
        if expected_params:
            # 使用正则表达式匹配参数
            for param_name in expected_params:
                param_pattern = rf"{param_name}=['\"](.*?)['\"]"
                param_match = re.search(param_pattern, params_str)
                if param_match:
                    params[param_name] = param_match.group(1)
        
        return {
            "type": action_type,
            "params": params
        }
    
    def execute_action(self, action_data):
        """
        模拟执行动作（仅打印结果）
        
        Args:
            action_data (dict): 解析后的动作数据
            
        Returns:
            str: 执行结果描述
        """
        if not action_data:
            return "没有可执行的动作"
        
        action_type = action_data["type"]
        params = action_data["params"]
        
        # 这里只是打印动作，实际实现中应该调用相应的函数
        param_str = ", ".join([f"{k}='{v}'" for k, v in params.items()])
        return f"执行动作: {action_type}({param_str})"


# 测试代码
if __name__ == "__main__":
    # 示例模型输出
    example_output = """Thought: 嗯，我看到了用户的问候，但这只是一个简单的打招呼，并没有明确的任务要求。作为一个负责任的助手，我需要请用户告诉我具体想要我帮忙做什么。让我问问用户："您好，请问有什么需要我帮忙的吗？"
Action: type(content='你好，请问有什么需要我帮忙的吗？')"""
    
    # 更复杂的示例
    complex_example = """Thought: 我看到屏幕上显示的是一个文件夹界面，需要打开其中的文档。我应该双击文档图标来打开它。
Action: left_double(start_box='[123, 456, 789, 987]')"""
    
    # 初始化解析器
    parser = UITarsParser()
    
    # 解析并执行简单示例
    print("示例1解析结果:")
    result1 = parser.parse_output(example_output)
    print(f"思考: {result1['thought']}")
    print(parser.execute_action(result1['action']))
    print("\n")
    
    # 解析并执行复杂示例
    print("示例2解析结果:")
    result2 = parser.parse_output(complex_example)
    print(f"思考: {result2['thought']}")
    print(parser.execute_action(result2['action'])) 