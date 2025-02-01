from flask import Flask, jsonify, request, render_template
import queue
import time
from vertex import multiturn_generate_content

app = Flask(__name__)

prompt = queue.Queue()
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    global chat_history
    data = request.get_json()
    user_message = data.get('userMessage', '')
    print(user_message)
    
    if not prompt:
        return jsonify({'reply': "no message received."}), 400
    try:
        prompt.put(user_message)
        print(f'added user message: {user_message}')

        response = None
        while response is None:
            time.sleep(1)
            if not prompt.empty():
                prompt_queue = prompt.get()
                response = multiturn_generate_content(prompt_queue, chat_history)
                print(response)
                print(f"Chat history: {chat_history}")
        return jsonify({'reply': response})
                  
    except Exception as e:
        print(f'exception in response {str(e)}')
        return f'exception {str(e)}'        


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8080, debug=False)
