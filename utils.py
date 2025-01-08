import json
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
load_dotenv(".env")


def save_messages(messages):
    with open('messages.json', 'w') as file:
        json.dump(messages, file)


def read_messages():
    with open('messages.json', 'r') as file:
        content = json.load(file)
        return content


def send_message(message):
    new_message = [{
        "role": "user",
        "content": message
    }]
    messages = read_messages()+new_message

    key = os.getenv("API_KEY")
    client = InferenceClient(api_key=key)

    completion = client.chat.completions.create(
        model="Qwen/QwQ-32B-Preview",
        messages=messages,
        max_tokens=500
    )
    response = {
        "role": "assistant",
        "content": completion.choices[0].message.content
    }
    messages.append(response)
    save_messages(messages)
    return messages


def print_chat(messages):
    messages.pop(0)
    all_content = []
    for message in messages:
        if message["role"] == 'user':
            all_content.append(f"- _{message["content"]}_")
        else:
            all_content.append(f"- __{message["content"]}__")
    return "\n".join(all_content)


def delete_messages():
    messages = read_messages()
    save_messages(messages[:1])
