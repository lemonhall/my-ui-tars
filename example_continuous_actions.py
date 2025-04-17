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
        """
        获取当前屏幕截图，或在缸中脑模式下返回None
        
        Returns:
            str|None: 截图路径或缸中脑模式下的None
        """
        if not self.use_screenshot:
            print("缸中脑模式：不使用屏幕截图")
            return None
        
        try:
            print("正在截取当前屏幕...")
            pyautogui.screenshot(self.screenshot_path)
            print(f"屏幕截图已保存至: {self.screenshot_path}")
            return self.screenshot_path
        except Exception as e:
            print(f"截图失败: {e}")
            return None
    
    def process_initial_task(self, task):
        """处理初始任务"""
        print(f"\n处理整体任务: {task}")
        
        # 获取初始截图
        screenshot_path = self.take_screenshot()
        
        # 初始任务处理
        result = self.agent.process_task(task, screenshot_path)
        
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
        screenshot_path = self.take_screenshot()
        
        # 处理任务
        result = self.agent.process_task(feedback, screenshot_path)
        
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

def run_session(mode="auto", use_screenshot=True):
    """
    运行会话，根据指定的模式和截图选项执行任务
    
    Args:
        mode (str): 会话模式，"auto"表示自动反馈，"interactive"表示交互式
        use_screenshot (bool): 是否使用截图，True使用实际截图，False为缸中脑模式
    """
    agent = MultiTurnAgent(use_screenshot=use_screenshot)
    
    # 使用模式文字描述
    mode_text = "交互式" if mode == "interactive" else "自动反馈"
    screenshot_text = "使用实际截图" if use_screenshot else "缸中脑模式(无截图)"
    
    print("="*50)
    print(f"UI-TARS {mode_text}会话 ({screenshot_text})")
    print("="*50)
    
    # 获取初始任务
    if mode == "interactive":
        # 交互式模式下通过输入获取任务
        initial_task = input("\n请输入整体任务: ")
        if initial_task.lower() in ['quit', 'exit']:
            return
    else:
        # 自动模式下使用预设任务
        initial_task = "打开记事本、输入一段文字、保存后关闭"
        print(f"\n使用预设任务: {initial_task}")
    
    # 处理初始任务
    result = agent.process_initial_task(initial_task)
    if not result:
        print("初始任务处理失败")
        return
    
    # 最大步骤数，防止无限循环
    max_steps = 10
    steps = 0
    
    if mode == "auto":
        print("\n开始执行自动反馈序列...")
    
    # 循环执行直到任务完成或达到最大步骤数
    while steps < max_steps:
        steps += 1
        
        if mode == "interactive":
            # 交互式模式下通过用户输入获取反馈
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
        else:
            # 自动模式下生成反馈
            last_action = agent.action_history[-1]
            feedback = agent.generate_feedback(last_action)
            
            print(f"\n--- 步骤 {steps}/{max_steps} ---")
            print(f"自动反馈: {feedback}")
            
            # 暂停一下，方便查看流程
            time.sleep(10)
        
        # 处理当前反馈
        result = agent.process_feedback(feedback)
        
        # 检查是否完成任务
        if result and result['action']['type'] == 'finished':
            print(f"\n任务已完成: {result['action']['params'].get('content', '任务完成')}")
            if mode == "interactive":
                cont = input("\n任务已标记为完成，是否继续? (y/n): ")
                if cont.lower() != 'y':
                    break
            else:
                break
    
    # 打印操作历史摘要
    agent.print_action_summary()

if __name__ == "__main__":
    import sys
    import argparse
    
    # 使用argparse解析命令行参数
    parser = argparse.ArgumentParser(description='UI-TARS多轮对话示例')
    parser.add_argument('--mode', choices=['auto', 'interactive'], default='auto',
                      help='运行模式：auto自动反馈，interactive交互式')
    parser.add_argument('--screenshot', choices=['true', 'false'], default='true',
                      help='是否使用截图：true使用实际截图，false缸中脑模式')
    
    args = parser.parse_args()
    
    mode = args.mode
    use_screenshot = args.screenshot.lower() == 'true'
    
    # 运行会话
    run_session(mode=mode, use_screenshot=use_screenshot) 