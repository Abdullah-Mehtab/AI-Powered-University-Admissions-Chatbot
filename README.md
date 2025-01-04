# AI-Powered University Admissions Chatbot

Welcome to the **AI-Powered University Admissions Chatbot**! This chatbot is designed to streamline the university admissions process by providing quick, accurate, and interactive answers to admission-related queries. It utilizes cutting-edge AI technologies, including Natural Language Processing (NLP) and Machine Learning (ML), to assist prospective students effectively.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Team Members](#team-members)
8. [License](#license)

## Introduction

The admissions process can be overwhelming with numerous questions about programs, deadlines, and scholarships. Traditional methods often fail to provide timely responses, leading to delays and frustration. This chatbot aims to:
- Reduce administrative workload.
- Provide accurate and instant responses.
- Enhance the user experience with a friendly, intuitive interface.

## Features

- **Instant Query Resolution**: Handles FAQs about admissions, scholarships, and deadlines with over 85% accuracy.
- **User-Friendly Interface**: Built with Tkinter for an interactive experience.
- **Smart NLP**: Understands user intent and generates context-aware responses.
- **Customizable Themes**: Includes a fun "Pink/UwU" mode.
- **Conversation Saving**: Allows users to save their chat history for reference.
- **Simple Arithmetic**: Supports basic arithmetic operations for added utility.

## Technologies Used

- **Python**: The core programming language.
- **TensorFlow & Keras**: For building and training the machine learning model.
- **NLTK**: For text preprocessing, including tokenization and lemmatization.
- **Tkinter**: For designing the graphical user interface.
- **JSON**: To structure intent data.

## Installation

### Prerequisites
- Python 3.8 or higher.
- Necessary libraries installed via `pip`.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/university-admissions-chatbot.git
   cd university-admissions-chatbot
   ```
2. Install dependencies:
   ```bash
   pip install tensorflow keras nltk
   ```
3. Set up the project directory:
   Place the following files in the root directory:
   - `intents.json`
   - `chatbot_model.h5`
   - `words.pkl`
   - `classes.pkl`

4. Run the chatbot:
   ```bash
   python chatbot.py
   ```

## Usage

1. Launch the chatbot using the steps above.
2. Type your questions in the input box and receive instant answers.
3. Toggle between themes and save your conversations as needed.

### Example Queries
- "What are the admission deadlines?"
- "Tell me about scholarships."
- "How can I apply for undergraduate programs?"

## Project Structure

```
university-admissions-chatbot/
├── chatbot.py            # Main chatbot script
├── training.py           # Script for training the ML model
├── intents.json          # Dataset of FAQs and responses
├── chatbot_model.h5      # Trained ML model
├── words.pkl             # Preprocessed word list
├── classes.pkl           # Preprocessed intent labels
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
```

## Team Members

- **Abdullah Mehtab**: Dataset preparation and model training.
- **Ali Mujtaba**: Interface development and information gathering.
- **Laiba**: Testing and evaluation.
- **Zain-ul-Abidin**: Quality assurance and additional features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to contribute or provide feedback! 😊
