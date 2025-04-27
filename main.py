from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Settings
model_names = ["qwen2.5:7b", "llama3.1", "gemma3", "gemma3_trading_analyst_0p1"]
base_url = "http://localhost:11434"  # Default for local Ollama


for model_name in model_names:
    # Initialize ChatOllama
    chat = ChatOllama(
        model=model_name,
        base_url=base_url,
    )

    # Send a message
    response = chat.invoke(
        [
            SystemMessage(
                content="You are a helpful trading analyst. Your job is to rate wheather a stock is a buy, hold or sell."
            ),
            HumanMessage(content="Hello! Who are you?"),
        ]
    )

    # Print the response
    print("model name: ", model_name)
    print(response.content)
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
