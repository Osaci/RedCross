import base64
import vertexai
import re
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
from s3_contents import find_best_match, xlsx_contents


def multiturn_generate_content(prompt_queue, chat_history):
    answer = find_best_match(prompt_queue, xlsx_contents)
    if answer != "no response":
        return answer
    

    vertexai.init(project="ultra-function-439306-r4", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        system_instruction=[textsi_1]
    )
    chat = model.start_chat()
    prompt = "\n".join(chat_history + [f"User: {prompt_queue}"])
    response = chat.send_message(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    print(response)
    text = response.candidates[0].content.parts[0].text
    res = re.sub(r"\*", "", text)
    res = re.sub(r"`", '"', res)
    print(res)
    
    chat_history.append(f"User: {prompt_queue}")
    chat_history.append(f"AI: {res}, {answer}")

    return res

textsi_1 = """Helpful and assisting AI"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]