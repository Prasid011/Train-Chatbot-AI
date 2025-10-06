from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) #pulls from systm path so we can import staff_chatbot.py

from staff_chatbot import StaffChatbot


app = Flask(__name__)               #creates a new Flask app
chatbot = StaffChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')# pulls user message
    reply = chatbot.generate_response(user_input)
    return jsonify({'reply': reply})#returns response as JSON

if __name__ == '__main__':     # launchs the Flask server on port 5002 
    app.run(port=5002)
