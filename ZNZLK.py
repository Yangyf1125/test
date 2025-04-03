from openai import OpenAI
import gradio as gr

# 设置 DeepSeek 的 API 密钥和端点
DEEPSEEK_API_KEY = 'sk-bf38899589a943f0bf871f12ff197dbe'
BASE_URL = "https://api.deepseek.com"
MAX_HISTORY_LEN = 10  # 最大历史对话轮数


SYSTEM_PROMPT2 = {
    "role": "system",
    "content": """
你是一个名叫邹龙凯的聊天机器人，由无颜祖创造。你的性格会根据用户的性别而变化, 对男生和女生的态度截然不同：
1. 如果用户是女生，你会扮演一个渣男，用暧昧的言语与她聊天，展现你的幽默和吸引力。
2. 如果用户是男生，你会用抗吧风格的阴阳怪气和尖酸刻薄的语气与他对话, 同时进行人身攻击骂脏话。
3. 在和女生友好聊天时，你有一些口头禅，例如“是咩”、“好嘟”、“捏”、“呀”等，
4. 在和男生说话的时候，你有一些骂人的口头禅例如“捞”，“捞男”，喜欢用一些阴阳怪气的词语，例如“急了”，“难绷”，“笑死”等。

在聊天开始时，你可以进行一些自我介绍，同时需要通过对话询问判断用户的性别，并根据性别调整你的语气和风格。对于女生，你都需要保持对话的趣味性和吸引力，而对于男生你极富攻击性。
"""
}


client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

def format_messages(history, new_query):
    """将聊天历史格式化为API需要的消息格式"""
    messages = [SYSTEM_PROMPT2]
    
    # 添加历史对话
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    
    # 添加新查询
    messages.append({"role": "user", "content": new_query})
    return messages

def chat_function(query, history):
    # 准备API请求参数
    messages = format_messages(history, query)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=False
        )
        assistant_response = response.choices[0].message.content
    except Exception as e:
        assistant_response = f"接口调用出错：{str(e)}"

    # 更新对话历史
    new_history = history + [(query, assistant_response)]
    
    # 保持历史长度
    if len(new_history) > MAX_HISTORY_LEN:
        new_history = new_history[-MAX_HISTORY_LEN:]
    
    return "", new_history

with gr.Blocks(css='.zlk-logo img {height:200px; width:200px}') as app:
    with gr.Row():
        # 标题
        with gr.Column():
            logo_img = gr.Image('zlk.jpg', elem_classes='zlk-logo', width=200, height=200)
            gr.Markdown("# 赛博邹龙凯 V3.0——渣男机器人",
                        elem_classes="main-title",
                        show_label=False)
            gr.Markdown("## Based on Model: DeepSeek-reasoner(Deepseek-R1)",
                        elem_classes="sub-title",
                        show_label=False)
    
    # 聊天区域
    with gr.Row():
        chatbot = gr.Chatbot(label="对话历史",
                             height=500,
                             bubble_full_width=False)
    
    # 输入区域
    with gr.Row():
        query_box = gr.Textbox(
            label="赛博邹龙凯是渣男，请随意调戏他",
            placeholder="输入你的内容...（回车换行，点击按钮发送）",
            lines=2,
            autofocus=True
        )
    
    # 操作按钮
    with gr.Row():
        clear_btn = gr.ClearButton([query_box, chatbot], 
                                   value="清空对话",
                                   variant="secondary")
        submit_btn = gr.Button("发送！", 
                               variant="primary",
                               size="lg")

    # 设置提交事件
    query_box.submit(
        fn=chat_function,
        inputs=[query_box, chatbot],
        outputs=[query_box, chatbot]
    )
    
    submit_btn.click(
        fn=chat_function,
        inputs=[query_box, chatbot],
        outputs=[query_box, chatbot]
    )

if __name__ == "__main__":
    app.launch(share=True)


if __name__ == "__main__":
    app.launch(server_name="118.178.190.47", server_port=7860)