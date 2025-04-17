from agno.agent import Agent, RunResponse
from agno.models.deepseek import DeepSeek
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage

#litellm初始化火山引擎的方法
#V3的模型
# llm = LLM(model="volcengine/ep-20250204220334-l2q5g", 
#           api_key=huoshan_key,temperature=0)

#R1的模型
# llm = LLM(model="volcengine/ep-20250204215316-p8rqb", 
#           api_key=huoshan_key,temperature=0)


# 使用 PowerShell
# 打开 PowerShell（在 “开始” 菜单中搜索 “PowerShell” 并打开）。
# 要为当前用户设置环境变量，可以使用
# $env:SILICONFLOW_API_KEY = "your_api_key"
# 命令。
# 同样，将"your_api_key"替换为实际的 API 密钥。不过，这种方式设置的环境变量只在当前 PowerShell 会话中有效。

# 要永久设置环境变量（对于当前用户），可以使用
# [Environment]::SetEnvironmentVariable("HUOSHAN_API_KEY","your_api_key","User")。
# 如果要设置系统级别的环境变量（需要管理员权限），可以将最后一个参数改为"Machine"，
# 例如
# [Environment]::SetEnvironmentVariable("HUOSHAN_API_KEY","your_api_key","Machine")。
# Set up SILICONFLOW API key
# 记得使用以上方法后，需要关闭vscode后重启vscode，之后点击F5运行python脚本的时候才能生效

V3 = "ep-20250204220334-l2q5g"
R1 = "ep-20250204215316-p8rqb"
TARS = "ep-20250417103958-d888s"

#参考官方文档：https://www.volcengine.com/docs/82379/1536429
#使用无随机性的推理参数，以提高模型输出准确性
# temperature=0
# top_p=0.7

ui_tars = DeepSeek(id=TARS,base_url="https://ark.cn-beijing.volces.com/api/v3/",temperature=0,top_p=0.7)

agent = Agent(model=ui_tars,
              name="我的UI助手",
              description="",
              instructions="""
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
            """,
            debug_mode=True,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
              )

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("starter:app", reload=True)