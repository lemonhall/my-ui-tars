#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI-TARS Agent 多轮对话操作示例
该脚本展示了如何使用UI-TARS Agent进行多轮对话式自动化操作
"""

from ui_tars_agent import UITarsAgent
import pyautogui
import json
import os
import time

class MultiTurnAgent:
    """多轮对话代理类，处理连续对话操作"""
    
    def __init__(self, use_screenshot=True):
        """
        初始化多轮对话代理
        
        Args:
            use_screenshot (bool): 是否使用实际截图，False表示缸中脑模式
        """
        print("初始化UI-TARS代理...")
        self.agent = UITarsAgent()
        self.screenshot_path = "current_screen.png"
        self.action_history = []  # 仅记录操作历史，不维护对话历史
        self.use_screenshot = use_screenshot
    
    def take_screenshot(self):
        """获取当前屏幕截图，或在缸中脑模式下跳过"""
        if not self.use_screenshot:
            print("缸中脑模式：跳过屏幕截图...")
            # 如果截图文件不存在，创建一个空白图像作为占位
            if not os.path.exists(self.screenshot_path):
                try:
                    # 创建一个1x1像素的黑色图像
                    from PIL import Image
                    img = Image.new('RGB', (800, 600), color = (0, 0, 0))
                    img.save(self.screenshot_path)
                    print(f"已创建空白图像: {self.screenshot_path}")
                except Exception as e:
                    print(f"创建空白图像失败: {e}")
                    return False
            return True
        
        try:
            print("正在截取当前屏幕...")
            pyautogui.screenshot(self.screenshot_path)
            print(f"屏幕截图已保存至: {self.screenshot_path}")
            return True
        except Exception as e:
            print(f"截图失败: {e}")
            return False
    
    def process_initial_task(self, task):
        """处理初始任务"""
        print(f"\n处理整体任务: {task}")
        
        # 获取初始截图
        if not self.take_screenshot():
            print("无法获取屏幕截图，退出任务")
            return None
        
        # 初始任务处理
        result = self.agent.process_task(task, self.screenshot_path)
        
        # 记录动作到历史
        self.action_history.append({
            "type": result["action"]["type"],
            "params": result["action"]["params"],
            "thought": result["thought"]
        })
        
        # 打印结果
        self._print_step_result(result)
        
        return result
    
    def process_feedback(self, feedback):
        """处理反馈并执行下一步操作"""
        if not self.action_history:
            print("没有活跃的任务，请先处理初始任务")
            return None
        
        # 更新截图
        self.take_screenshot()
        
        # 处理任务
        result = self.agent.process_task(feedback, self.screenshot_path)
        
        # 记录动作到历史
        self.action_history.append({
            "type": result["action"]["type"],
            "params": result["action"]["params"],
            "thought": result["thought"]
        })
        
        # 打印结果
        self._print_step_result(result)
        
        return result
    
    def _print_step_result(self, result):
        """打印步骤结果"""
        print("\n==================== 步骤结果 ====================")
        print(f"模型思考: {result['thought']}")
        print(f"执行动作: {json.dumps(result['action'], ensure_ascii=False)}")
        print(f"执行结果: {json.dumps(result['execution'], ensure_ascii=False)}")
        print("=================================================\n")
    
    def print_action_summary(self):
        """打印操作历史摘要"""
        print("\n============= 操作历史摘要 =============")
        for i, action in enumerate(self.action_history):
            params_str = ""
            if "params" in action and action["params"]:
                for k, v in action["params"].items():
                    if isinstance(v, str) and len(v) > 20:
                        v = v[:17] + "..."
                    params_str += f"{k}={v}, "
                params_str = params_str.rstrip(", ")
            
            print(f"[{i+1}] {action['type']}({params_str})")
        print("========================================")
    
    def generate_feedback(self, action):
        """根据action类型生成自动反馈"""
        action_type = action["type"]
        params = action["params"] if "params" in action else {}
        
        feedback_templates = {
            "click": "点击操作已完成，点击的位置是{start_box}",
            "left_double": "双击操作已完成，双击的位置是{start_box}",
            "right_single": "右键点击已完成，点击的位置是{start_box}",
            "drag": "拖拽操作已完成，从{start_box}拖动到{end_box}",
            "hotkey": "热键{key}已按下",
            "type": "文本已输入：{content}",
            "scroll": "已在{start_box}位置向{direction}方向滚动",
            "wait": "等待操作完成，已暂停5秒",
            "finished": "任务已完成：{content}"
        }
        
        if action_type in feedback_templates:
            template = feedback_templates[action_type]
            try:
                # 尝试格式化模板
                feedback = template.format(**params)
            except KeyError:
                # 如果格式化失败，返回通用反馈
                feedback = f"{action_type}操作已完成"
        else:
            feedback = f"{action_type}操作已完成"
        
        return feedback

def run_auto_feedback_scenario(use_screenshot=True):
    """运行自动反馈场景"""
    agent = MultiTurnAgent(use_screenshot=use_screenshot)
    
    # 整体任务
    initial_task = "打开记事本、输入一段文字、保存后关闭"
    
    # 处理初始任务
    result = agent.process_initial_task(initial_task)
    if not result:
        print("初始任务处理失败")
        return
    
    # 最大步骤数，防止无限循环
    max_steps = 10
    steps = 0
    
    print("\n开始执行自动反馈序列...")
    
    # 循环执行直到任务完成或达到最大步骤数
    while steps < max_steps:
        steps += 1
        
        # 根据最后一个动作生成反馈
        last_action = agent.action_history[-1]
        feedback = agent.generate_feedback(last_action)
        
        print(f"\n--- 步骤 {steps}/{max_steps} ---")
        print(f"自动反馈: {feedback}")
        
        # 暂停一下，方便查看流程
        time.sleep(5)
        
        # 处理当前反馈
        result = agent.process_feedback(feedback)
        
        # 检查是否完成任务
        if result and result['action']['type'] == 'finished':
            print(f"\n任务已完成: {result['action']['params'].get('content', '任务完成')}")
            break
    
    # 打印操作历史摘要
    agent.print_action_summary()

def run_braininavat_scenario():
    """运行缸中脑模式（无截图+自动反馈）"""
    print("\n========== 缸中脑模式启动 ==========")
    print("在这个模式下，模型不使用实际截图，而是凭借对话历史和反馈进行推理")
    print("======================================\n")
    
    # 调用自动反馈场景但不使用截图
    run_auto_feedback_scenario(use_screenshot=False)

def interactive_mode(use_screenshot=True):
    """交互式模式"""
    agent = MultiTurnAgent(use_screenshot=use_screenshot)
    
    mode_desc = "标准" if use_screenshot else "缸中脑(无截图)"
    
    print("="*50)
    print(f"UI-TARS 交互式多轮对话模式 ({mode_desc})")
    print("输入'quit'或'exit'退出, 'summary'查看操作历史, 'auto'使用自动反馈")
    print("="*50)
    
    # 获取初始任务
    initial_task = input("\n请输入整体任务: ")
    if initial_task.lower() in ['quit', 'exit']:
        return
    
    # 处理初始任务
    result = agent.process_initial_task(initial_task)
    if not result:
        print("初始任务处理失败")
        return
    
    # 交互式对话循环
    while True:
        # 获取用户反馈
        feedback = input("\n请输入执行结果或下一步指令 ('quit'退出, 'summary'查看历史, 'auto'使用自动反馈): ")
        
        if feedback.lower() in ['quit', 'exit']:
            break
        elif feedback.lower() == 'summary':
            agent.print_action_summary()
            continue
        elif feedback.lower() == 'auto':
            # 使用自动生成的反馈
            last_action = agent.action_history[-1]
            feedback = agent.generate_feedback(last_action)
            print(f"使用自动反馈: {feedback}")
        
        # 处理反馈
        result = agent.process_feedback(feedback)
        
        # 检查是否完成任务
        if result and result['action']['type'] == 'finished':
            print(f"\n任务已完成: {result['action']['params'].get('content', '任务完成')}")
            cont = input("\n任务已标记为完成，是否继续? (y/n): ")
            if cont.lower() != 'y':
                break

if __name__ == "__main__":
    import sys
    
    # 根据命令行参数决定运行模式
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_mode(use_screenshot=True)
        elif sys.argv[1] == "--auto":
            run_auto_feedback_scenario(use_screenshot=True)
        elif sys.argv[1] == "--brain-in-vat":
            run_braininavat_scenario()
        elif sys.argv[1] == "--interactive-brain":
            interactive_mode(use_screenshot=False)
    else:
        # 默认运行缸中脑模式
        run_braininavat_scenario() 