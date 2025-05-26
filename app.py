from flask import Flask, render_template, request
import ollama

app = Flask(__name__)

def get_response_from_ollama(user_input):
    # Get the response from the locally running Ollama model
    response = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": user_input}])
    print(response)

    if 'message' in response:
        content = response['message']['content']
        # Remove <think> tags from the response
        cleaned_content = content.replace("<think>", "").replace("</think>", "").strip()
        return cleaned_content
    
    else:
        return 'Sorry, something went wrong.'


@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    bot_response = ""
    
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = get_response_from_ollama(user_input)
    
    return render_template("index.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
