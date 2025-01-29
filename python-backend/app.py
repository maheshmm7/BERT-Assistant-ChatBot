from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json
import torch
from textblob import TextBlob
import datetime
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the SBERT model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load the database of intents and responses
with open('database.json', 'r') as f:
    intents = json.load(f)

# Encode the patterns for all intents
intent_encodings = {}
for intent in intents['intents']:
    tag = intent['tag']
    patterns = intent['patterns']
    intent_encodings[tag] = model.encode(patterns, convert_to_tensor=True)

def correct_spelling(user_input):
    blob = TextBlob(user_input)
    corrected_text = str(blob.correct())
    return corrected_text

def predict_tag(sentence, threshold=0.5):
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    
    max_similarity = -1
    predicted_tag = None

    for tag, encodings in intent_encodings.items():
        cosine_scores = util.pytorch_cos_sim(sentence_embedding, encodings)
        max_score = torch.max(cosine_scores).item()
        
        if max_score > max_similarity:
            max_similarity = max_score
            predicted_tag = tag

    if max_similarity < threshold:
        return "unknown"

    return predicted_tag

def get_response(predicted_tag):
    if predicted_tag == "unknown":
        return ["Sorry, I didn't understand that. Could you please rephrase?"]

    for intent in intents['intents']:
        if intent['tag'] == predicted_tag:
            return intent['responses']
    return ["Sorry, I don't understand that."]

def log_chat(user_input, corrected_input, response):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - User Input: {user_input} | Corrected Input: {corrected_input} | Response: {response}\n"
    
    with open('chat_log.txt', 'a') as log_file:
        log_file.write(log_entry)

@app.route('/')
def home():
    return "Chatbot is running."

@app.route('/api/chat', methods=['POST'])  # Changed route to /api/chat
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify(response="Please provide a valid input."), 400

        corrected_input = correct_spelling(user_input)
        predicted_tag = predict_tag(corrected_input)
        response = get_response(predicted_tag)

        log_chat(user_input, corrected_input, response[0])

        return jsonify(response=response[0], corrected_input=corrected_input)
    except Exception as e:
        return jsonify(response="An error occurred: {}".format(str(e))), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True, threaded=True)
