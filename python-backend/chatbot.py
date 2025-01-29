import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import json
import random

# Load the trained model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained("customer_care_bert_model")
tokenizer = DistilBertTokenizer.from_pretrained("customer_care_bert_tokenizer")

# Load the database of intents and responses
with open('database.json', 'r') as f:
    intents = json.load(f)

# Set the model to evaluation mode
model.eval()

# Device configuration (use GPU if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Function to predict the tag for a given input sentence
def predict_tag(sentence):
    inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted label (tag index)
    _, predicted = torch.max(outputs.logits, dim=1)
    predicted_tag_index = predicted.item()

    return predicted_tag_index

# Function to get the response for the predicted tag
def get_response(tag_index):
    if tag_index < len(intents['intents']):
        tag = intents['intents'][tag_index]['tag']
        for intent in intents['intents']:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])  # Return a random response
    return "Sorry, I don't understand that."

# Chatbot loop
def chatbot():
    print("Start chatting with the bot (type 'quit' to stop)!")

    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == "quit":
            print("Chatbot: Goodbye!")
            break
        
        # Predict the tag for the user input
        predicted_tag_index = predict_tag(user_input)
        
        # Get the response for the predicted tag
        response = get_response(predicted_tag_index)

        # Print the predicted tag for debugging
        predicted_tag = intents['intents'][predicted_tag_index]['tag']
        print(f"Predicted tag: {predicted_tag}")

        # Print the chatbot response
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()
