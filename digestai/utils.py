import os
import openai

def get_summary(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f'\"{text}\"\n\n\nSummarize the above text.'
    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=prompt,
        temperature=0.92,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.4,
        presence_penalty=0.0,
        stop=["\"\"\""]
        )
    return response['choices'][0]['text']

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions