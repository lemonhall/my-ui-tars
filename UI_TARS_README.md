# UI-TARS 解析器和执行器

## 项目简介

这是一个基于 [Agno](https://github.com/agumelar/agno) 框架的UI-TARS模型输出解析和执行工具。该工具可以将UI-TARS多模态模型的输出解析为结构化数据，并执行相应的UI自动化操作。

## 功能特点

- 解析UI-TARS模型输出的思考和动作部分
- 支持将解析后的动作转换为实际的UI操作
- 支持多种UI交互操作（点击、双击、右键点击、拖拽、热键、输入文本等）
- 提供交互式界面用于执行UI自动化任务
- 支持屏幕截图输入和实时执行反馈

## 文件说明

本项目包含以下主要文件：

- `ui_tars_parser.py`: UI-TARS模型输出解析器
- `ui_tars_executor.py`: UI操作执行器
- `ui_tars_agent.py`: 基于Agno框架的UI-TARS代理
- `main.py`: 主程序，整合解析器、执行器和代理
- `example.py`: 示例脚本，演示如何使用解析器和执行器

## 安装指南

### 前提条件

- Python 3.12 或更高版本
- 开通火山引擎上UI-TARS的对应权限，创建对应的接入点，得到模型名称以及API-KEY

### 安装步骤

1. 确保已安装必要的依赖：

```bash
pip install pyautogui agno
```

2. 设置火山引擎API密钥：

Windows (PowerShell)：
```powershell
[Environment]::SetEnvironmentVariable("HUOSHAN_API_KEY", "your_api_key", "User")
```

Linux/macOS：
```bash
export HUOSHAN_API_KEY="your_api_key"
echo 'export HUOSHAN_API_KEY="your_api_key"' >> ~/.bashrc  # 永久保存
```

## 使用说明

### 解析器和执行器示例

可以使用 `example.py` 脚本来测试解析器和执行器的功能：

```bash
python example.py
```

这将执行预定义的三个示例操作：点击、键盘输入和热键操作。

### 交互式UI自动化

通过 `main.py` 可以启动交互式UI自动化助手：

```bash
python main.py
```

交互式会话允许您：
- 输入任务描述
- 选择是否使用屏幕截图
- 查看模型思考和动作解析结果
- 实时执行UI自动化操作

### API使用示例

#### 解析UI-TARS模型输出

```python
from ui_tars_parser import UITarsParser

# 初始化解析器
parser = UITarsParser()

# 示例模型输出
model_output = """Thought: 我需要点击屏幕上的"开始"按钮，它位于屏幕左下角的位置。
Action: click(start_box='[17, 980, 50, 990]')"""

# 解析输出
result = parser.parse_output(model_output)
print(result)
```

#### 执行UI自动化操作

```python
from ui_tars_executor import UITarsExecutor

# 初始化执行器
executor = UITarsExecutor()

# 定义动作
action = {
    "type": "click",
    "params": {
        "start_box": "[500, 500, 550, 550]"
    }
}

# 执行动作
result = executor.execute(action)
print(result)
```

## 注意事项

- 使用UI自动化操作时，请确保您有足够的时间切换到正确的窗口
- UI-TARS模型输出的坐标是相对坐标，需要转换为绝对坐标
- 设置环境变量后，可能需要重启应用程序或终端才能生效
- 坐标转换遵循以下规则：
  - X绝对坐标 = X相对坐标 × 屏幕宽度 / 1000
  - Y绝对坐标 = Y相对坐标 × 屏幕高度 / 1000 