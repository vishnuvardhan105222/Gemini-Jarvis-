


from flask import Flask, jsonify, request, render_template
from agent import run_conversation

app = Flask(__name__)

@app.route("/process_message", methods=["POST"])
def process_message_func1():
    msg = request.json.get('message')
    if msg:
        print("Received message:", msg)
        resp = run_conversation(msg)
        return jsonify({"response": resp})
    else:
        return jsonify({"error": "No message provided"}), 400

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


 
