import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet


with open('dialogues.json', 'r') as f:
    dialogues = json.load(f)

all_words = []
tags = []
xy = [] #holds both patterns and texts

# loop through each sentence in our dialogues patterns
for dialogue in dialogues['dialogues']:
    tag = dialogue['tag']
    # add to tag list
    tags.append(tag)

    for pattern in dialogue['patterns']:

        # tokenize each word in the sentence
        w = tokenize(pattern)

        # add to our words list
        all_words.extend(w) #because we want to add values in array and not an array in the array

        # add to xy pair
        xy.append((w, tag))

ignore_words = ['?', '.', '!']

#converting all the words in lower case and do stemming simultaneously
all_words = [stem(w) for w in all_words if w not in ignore_words]

# remove duplicates and sort
#set removes the duplicate words from the list
all_words = sorted(set(all_words))
tags = sorted(set(tags)) 
print(tags)

# print(len(xy), "patterns")
# print(len(tags), "tags:", tags)
# print(len(all_words), "unique stemmed words:", all_words)

# create training data
X_train = []
y_train = []

for (pattern_sentence, tag) in xy:

    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

