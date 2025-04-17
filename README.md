# my-ui-tars

## 项目简介

my-ui-tars 是一个基于 [Agno](https://github.com/agumelar/agno) 框架的UI自动化助手项目。该项目使用多模态模型UI-TARS（基于qwen-vl系列微调后的视觉模型）来解释屏幕截图并执行UI操作，实现计算机界面的自动化交互。

## 功能特点

- 使用多模态模型UI-TARS（基于qwen-vl系列微调后的视觉模型））理解屏幕内容
- 支持多种UI交互操作（点击、双击、右键点击、拖拽、热键、输入文本等）
- 提供可视化的Playground界面用于开发和测试
- 支持操作历史记录和上下文理解

## 技术栈

- Python 3.12+
- Agno 框架 (≥1.3.2)
- FastAPI (≥0.115.12)
- OpenAI 库 (≥1.75.0)
- SQLAlchemy (≥2.0.40)
- Uvicorn (≥0.34.1)
- PyAutoGUI (≥0.9.54)
- PyGetWindow (≥0.0.9)
- PyYAML (≥6.0.1)
- Pillow (≥10.2.0)
- DeepSeek 模型 API（但实际链接的为字节跳动，火山引擎下的UI-TARS模型，该模型为qwen-vl视觉模型系列）

## 安装指南

### 前提条件

- Python 3.12 或更高版本
- 开通 火山引擎上UI-TARS的 对应权限，创建对应的接入点，得到 模型名称 以及API-KEY等

### 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/my-ui-tars.git
cd my-ui-tars
```

2. 创建并激活虚拟环境：

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. 安装依赖：

```bash
pip install -e .
# 或者手动安装依赖
pip install agno>=1.3.2 fastapi>=0.115.12 openai>=1.75.0 sqlalchemy>=2.0.40 uvicorn>=0.34.1 pyautogui>=0.9.54 pygetwindow>=0.0.9 pyyaml>=6.0.1 pillow>=10.2.0
```

4. 配置 DeepSeek API 密钥：

Windows (PowerShell)：
```powershell
[Environment]::SetEnvironmentVariable("HUOSHAN_API_KEY", "your_api_key", "User")
```

Linux/macOS：
```bash
export DEEPSEEK_API_KEY="your_api_key"
echo 'export HUOSHAN_API_KEY="your_api_key"' >> ~/.bashrc  # 永久保存
```

## 使用说明

1. 启动应用：

```bash
python starter.py
```

2. 根据命令行中的提示，打开浏览器访问 Playground：

```
http://localhost:8000
```

3. 在 Playground 界面上，您可以：
   - 上传屏幕截图
   - 输入任务指令
   - 查看 AI 助手推理过程
   - 执行 UI 自动化操作


## 官方提示词：

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
      type(content='') #If you want to submit your input, use "\n" at the end of `content`.
      scroll(start_box='[x1, y1, x2, y2]', direction='down or up or right or left')
      wait() #Sleep for 5s and take a screenshot to check for any changes.
      finished(content='xxx') # Use escape characters \\', \\", and \\n in content part to ensure we can parse the content in normal python string format.
      ## Note
      - Use Chinese in `Thought` part.
      - Write a small plan and finally summarize your next action (with its target element) in one sentence in `Thought` part.
      ## User Instruction

## 代理操作指令集

以下是整理成Markdown格式的Action集表格：

```markdown
| Action名称   | 动作类型     | 参数                     | 输出示例                                                                 |
|-------------|-------------|--------------------------|-------------------------------------------------------------------------|
| click       | 点击         | start_box               | `click(start_box='<bbox>859 950 859 950</bbox>')`                      |
| left_double | 左键双击     | start_box               | `left_double(start_box='<bbox>859 950 859 950</bbox>')`                 |
| right_single| 右键单击     | start_box               | `right_single(start_box='<bbox>859 950 859 950</bbox>')`                |
| drag        | 拖拽         | start_box \n end_box    | `drag(start_box='<bbox>768 150 768 150</bbox>', end_box='<bbox>79 150 79 150</bbox>')` |
| hotkey      | 热键         | key                     | `hotkey(key='ctrl a')`                                                  |
| type        | 键盘输入     | content                 | `type(content='北京天气怎么样')`                                        |
| scroll      | 滚动屏幕     | start_box<br>direction  | `scroll(direction='up', start_box='<bbox>850 869 850 869</bbox>')`      |
| wait        | 等待         |                         | `wait()`                                                               |
| finished    | 完成         | content                 | `finished(content='todo.txt已打开')`                                   |
```


## 模型输出坐标值说明：

https://www.volcengine.com/docs/82379/1536429


Action坐标映射

**该模型生成的二维坐标输出表示相对位置。**要将这些值转换为相对于图像的坐标，需将每个分量除以1000，得到范围在[0,1]内的值。动作所需的绝对坐标可通过以下公式计算：

X绝对坐标 = X相对坐标 × 图像宽度 
Y绝对坐标 = Y相对坐标 × 图像高度 


例如：

给定屏幕尺寸为1920 × 1080
模型生成的坐标输出为(235, 512)
则
X绝对坐标为：round(1920*235/1000)=451
Y绝对坐标为：round(1080*512/1000)=553
最终得到的绝对坐标为(451, 553)

## 系统设计原则

本项目遵循单一职责原则，将系统功能划分为多个模块，每个模块负责特定的功能：

1. **UITarsAgent (ui_tars_agent.py)**
   - 负责与模型进行交互
   - 处理用户任务和截图输入
   - 管理整体工作流程
   - 调用解析器和执行器组件

2. **UITarsParser (ui_tars_parser.py)**
   - 负责解析模型生成的文本输出
   - 提取思考过程和动作指令
   - 将文本格式的动作转换为结构化数据

3. **UITarsExecutor (ui_tars_executor.py)**
   - 负责执行实际的UI操作
   - 处理坐标转换（从相对坐标到绝对坐标）
   - 封装所有与屏幕交互相关的功能
   - 实现各种操作（点击、拖拽、输入等）

这种模块化设计有以下优势：
- 每个组件职责明确，代码更易于维护
- 组件之间松耦合，方便单独测试和替换
- 避免功能重复，如坐标转换只在执行器中实现

## 许可证

[请添加许可证信息]

## 贡献指南

[可选：添加贡献指南]