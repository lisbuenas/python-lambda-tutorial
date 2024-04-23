from firebase_functions import https_fn
from firebase_admin import initialize_app
from flask import Flask
from openai import OpenAI
app = Flask(__name__)

client = OpenAI(
  api_key='CHATPT_KEY',
)
completion_model = "gpt-3.5-turbo-0613"

initialize_app()

def generate_description(req):
    request_json = req.get_json()
    description = request_json['description']
    question = "Describe the following word: " +  description + "."
    messages = [{"role": "user", "content": question}]
    
    try:
        response = client.chat.completions.create(
            model=completion_model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content

    except Exception as e:
        print("An error occurred:", e)
        return None
   
@https_fn.on_request(max_instances=1)
def handle_post_request(req: https_fn.Request) -> https_fn.Response:
    response_data = generate_description(req)
    return https_fn.Response(response_data, content_type="application/json")