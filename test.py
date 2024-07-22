import random
import json
import torch
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sera"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.15:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand..."

def init_db():
    conn = sqlite3.connect('chatbot.db')
    return conn

def save_message(user_id, message, sender):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_id, message, sender) VALUES (?, ?, ?)", (user_id, message, sender))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT message, sender, timestamp FROM chats WHERE user_id = ? ORDER BY timestamp", (user_id,))
    chat_history = cursor.fetchall()
    conn.close()
    return chat_history

@app.route('/')
def home():
    if 'user_id' in session:
        chat_history = get_chat_history(session['user_id'])
        return render_template('index.html', chat_history=chat_history)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    if 'user_id' not in session:
        return jsonify({"response": "User not logged in."}), 401
    
    user_input = request.json.get('msg')  # Use .json.get() for JSON requests
    user_id = session['user_id']
    
    save_message(user_id, user_input, "You")
    
    bot_response = get_response(user_input)
    save_message(user_id, bot_response, bot_name)
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, request, jsonify, render_template
# import random
# import json
# import torch
# from model import NeuralNet
# from nltk_utils import bag_of_words, tokenize

# app = Flask(__name__)

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# with open('intents.json', 'r') as f:
#     intents = json.load(f)

# FILE = "data.pth"
# data = torch.load(FILE)

# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data["all_words"]
# tags = data["tags"]
# model_state = data["model_state"]

# model = NeuralNet(input_size, hidden_size, output_size).to(device)
# model.load_state_dict(model_state)
# model.eval()

# bot_name = "Sera"

# def get_response(msg):
#     sentence = tokenize(msg)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output = model(X)
#     _, predicted = torch.max(output, dim=1)

#     tag = tags[predicted.item()]

#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.05:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 return random.choice(intent['responses'])
    
#     return "I do not understand..."

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')
#     response = get_response(user_input)
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     app.run(debug=True)
