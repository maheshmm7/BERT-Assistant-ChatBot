import os
import json
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader, random_split
from sentence_transformers import SentenceTransformer, util

# Load intents data from the database.json file
with open('database.json', 'r') as f:
    intents = json.load(f)

# Prepare the data
tags = []
xy = []  # A list to hold (pattern, tag) pairs
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        xy.append((pattern, tag))

# Initialize SBERT model (Sentence-BERT)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Get all patterns and their corresponding tags
all_patterns = [pattern for pattern, _ in xy]
all_tags = [tags.index(tag) for _, tag in xy]

# Precompute embeddings for all patterns
pattern_embeddings = model.encode(all_patterns, convert_to_tensor=True)

# Create a dataset class for SBERT
class ChatDataset(Dataset):
    def __init__(self, patterns, tags):
        self.patterns = patterns
        self.tags = tags

    def __getitem__(self, idx):
        return self.patterns[idx], self.tags[idx]

    def __len__(self):
        return len(self.tags)

# Create a dataset
dataset = ChatDataset(all_patterns, all_tags)

# Split dataset into training and validation sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# DataLoader for batching (use batch_size=1 for embedding comparison)
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)

# Training loop for SBERT (no traditional fine-tuning, just embedding comparison)
num_epochs = 20
best_val_loss = float('inf')

# Define loss function for cosine similarity
def cosine_loss(embeddings, target_idx):
    cosine_scores = util.cos_sim(embeddings, pattern_embeddings)
    predicted_idx = torch.argmax(cosine_scores, dim=1).item()
    return 1.0 - cosine_scores[0][target_idx].item(), predicted_idx

# Training loop
for epoch in range(num_epochs):
    model.train()  # SBERT doesn't require typical fine-tuning

    epoch_loss = 0.0
    correct = 0
    total = 0

    for pattern, target_idx in train_loader:
        # Compute embeddings for the current pattern (from DataLoader)
        pattern_embedding = model.encode(pattern[0], convert_to_tensor=True)

        # Compute loss (1 - cosine similarity between predicted and target)
        loss, predicted_idx = cosine_loss(pattern_embedding, target_idx.item())

        # Update loss and accuracy metrics
        epoch_loss += loss
        if predicted_idx == target_idx:
            correct += 1
        total += 1

    avg_epoch_loss = epoch_loss / len(train_loader)
    accuracy = correct / total

    # Validation phase
    model.eval()
    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for pattern, target_idx in val_loader:
            # Compute embeddings for the current validation pattern
            pattern_embedding = model.encode(pattern[0], convert_to_tensor=True)

            # Compute loss and predicted index
            loss, predicted_idx = cosine_loss(pattern_embedding, target_idx.item())
            val_loss += loss

            if predicted_idx == target_idx:
                val_correct += 1
            val_total += 1

    avg_val_loss = val_loss / len(val_loader)
    val_accuracy = val_correct / val_total

    # Save the best model based on validation loss
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        model.save('customer_care_sbert_model')

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_epoch_loss:.4f}, Accuracy: {accuracy:.4f}, '
          f'Val Loss: {avg_val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}')

print("Training complete. Model saved.")
