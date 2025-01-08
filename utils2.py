import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv(".env")


def create_image(prompt: str, title: str = "image"):
    """
    Generate an image from a prompt.
    """
    img_key = os.getenv("API_KEY")
    img_client = InferenceClient(
        "stabilityai/stable-diffusion-xl-base-1.0", token=img_key)
    image = img_client.text_to_image(prompt)
    image.save(f"{title}.png")
    return (image, title)


def chat(prompt):
    key = os.getenv("API_KEY")
    client = InferenceClient(api_key=key)
    tools = [
        {"type": "function",
         "function": {
             "name": "create_image",
             "description": "Generate an image based on a given text prompt.",
             "parameters": {
                 "type": "object",
                 "properties": {
                     "prompt": {"type": "string", "description": "The text description of the image."},
                     "title": {"type": "string", "description": "A title for te image"}
                 },
                 "required": ["prompt"]
             }
         }
         }
    ]
    functions = {
        "create_image": create_image
    }
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="microsoft/Phi-3.5-mini-instruct",
        messages=messages,
        tools=tools,
        max_tokens=500
    )

    tool_calls = completion.choices[0].message.tool_calls

    if tool_calls:
        for tool in tool_calls:
            to_call = functions.get(tool.function.name)
            output = to_call(**tool.function.arguments)
            return output

    else:
        return completion.choices[0].message
