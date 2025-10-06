from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) #pulls from systm path so we can import customer_chatbot.py

from chatbot_app import TrainTicketChatbotWithBooking


app = Flask(__name__)
chatbot = TrainTicketChatbotWithBooking()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')# pulls user message
    reply = chatbot.generate_response(user_input)
    return jsonify({'reply': reply})#returns response as JSON

if __name__ == '__main__':       # launchs the Flask server on port 5001
    app.run(port=5001)
