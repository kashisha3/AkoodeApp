# AkoodeApp

Welcome to the AkoodeApp project repository! This chatbot application is designed to provide an interactive and personalized experience with user authentication and chat history management.

This chatbot application is designed to provide an interactive and personalized experience with user authentication and chat history management. Built using Python, Flask, and PyTorch, the application allows users to register and log in, ensuring that their chat sessions are secure and personalized. Once logged in, users can interact with the chatbot, and their conversations are stored in a SQLite database, enabling them to retrieve previous chats upon subsequent logins. The frontend is developed using HTML templates with Flask’s templating engine, providing a seamless user interface that includes login, registration, and chat functionalities. The chatbot's responses are generated using a neural network model trained on specific intents, making it capable of responding appropriately to various user queries.


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologiesused)
- [Contributors](#contributors)


## Introduction

The AkoodeApp is an intelligent chatbot application built using Python, Flask, and PyTorch. It allows users to register and log in, ensuring that their chat sessions are secure and personalized. Once logged in, users can interact with the chatbot, and their conversations are stored in a SQLite database, enabling them to retrieve previous chats upon subsequent logins. The frontend is developed using HTML templates with Flask’s templating engine, providing a seamless user interface that includes login, registration, and chat functionalities. The chatbot's responses are generated using a neural network model trained on specific intents, making it capable of responding appropriately to various user queries.


## Features

1. **User Authentication:** Secure login and registration system.
2. **Chat History:** Stores and retrieves chat history for each user.
3. **Interactive Chatbot:** Neural network-based responses for user queries.
4. **Responsive UI:** Visually appealing interface using HTML, CSS, and Bootstrap.


## Requirements
- Python 3.x
- Flask Version: 2.0.1
- PyTorch
- SQLite
- NLTK
- npm
- pip


## Installation

To get a local copy up and running, follow these simple steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/kashisha3/AkoodeApp.git
    ```
2. **Navigate to the project directory:**
    ```sh
    cd AkoodeApp
    ```

3. **Install Python dependencies:**
   ```sh
    pip install -r requirements.txt

    ```
4. **Install npm dependencies:**
   ```sh
    npm install
 
   ```
5. **Install Flask**
   ```sh
   pip install Flask==2.0.2

   ```
6. **Install PyTorch:**
   ```sh
   pip install torch
   ```


## Usage

Update the intents.json file: Add the questions and answers you want (or use the demo dataset).
1. Train the model:
sh
```
python train.py
```
2. Run the application:
sh
```
python test.py
```
3. Open your browser and navigate to the local host link provided in the terminal.
4. Register or login: If you are a new user, your data will be saved in the chatbot.db file.
5. Chat with the chatbot and enjoy the interactive experience.

## Technologies Used

1. Frontend: HTML, CSS, Bootstrap
2. Backend: Python, Flask
3. Database: SQLite
4.  Machine Learning: PyTorch
5. Natural Language Processing: NLTK library
6. Other tools: npm(Node Package Managaer), pip(Python Package installer)
   
## Contributors
- Kahsish Arora 
- Liza

This project was completed as a summer internship software development project under Akoode Technology.

