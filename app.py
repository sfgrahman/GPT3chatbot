from flask import Flask, render_template, request
import openai
import config

openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['JAX:', 'USER:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text


def handle_user_input(user_input):
    conversation = list()
    while True:
        # user_input = input('USER: ')
        conversation.append('USER: %s' % user_input)
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\JOY:'
        response = gpt3_completion(prompt)
        #print('JOY:', response)
        conversation.append('JOY: %s' % response)
        return response


@app.route("/")
def home():
    return render_template("index2.html")
 

@app.route("/get")
def bot_response():
    user_message = request.args.get('msg')
    return str(handle_user_input(user_message))


if __name__ == "__main__":
    app.run()
 