import random, time
import re
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tkinter as tk
from tkinter import filedialog
from tensorflow import keras
import threading  # For updating tips asynchronously

import warnings # General Warning suppression
warnings.filterwarnings('ignore')
import os # Suppress TensorFlow messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  


# --------------- SETUP NLTK ---------------
nltk.data.path.append("nltk_data")
nltk.download('punkt', download_dir="nltk_data")
nltk.download('wordnet', download_dir="nltk_data")

lemmatizer = WordNetLemmatizer()

# --------------- LOAD INTENTS, WORDS, CLASSES, MODEL ---------------
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open("classes.pkl", "rb"))
model = keras.models.load_model('chatbot_model.h5')

# --------------- NLP HELPER FUNCTIONS ---------------
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]
    return return_list

def get_response(intents_list, intents_data):
    """
    Return a random response based on the top predicted intent
    """
    if not intents_list:
        return "I'm sorry, but I don't have a response for that."
    tag = intents_list[0]['intent']
    for intent in intents_data:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I'm sorry, but I don't have a response for that."

# --------------- SIMPLE ARITHMETIC CHECK ---------------
def check_arithmetic(message):
    """
    Checks if the user input matches the pattern: number [+-x/] number
    Returns the arithmetic result as a string if matched, else None.
    """
    # Regex: one or more digits (with optional decimal), optional spaces,
    # a symbol (+, -, x, /), optional spaces, then one or more digits
    pattern = r'^(\d+(?:\.\d+)?)\s*([\+\-x/])\s*(\d+(?:\.\d+)?)$'
    match = re.match(pattern, message.strip())
    if match:
        # Extract the parts
        num1 = float(match.group(1))
        operator = match.group(2)
        num2 = float(match.group(3))

        # Perform the calculation
        if operator == '+':
            return str(num1 + num2)
        elif operator == '-':
            return str(num1 - num2)
        elif operator in ['x', '*']:
            return str(num1 * num2)
        elif operator == '/':
            if num2 == 0:
                return "Error: Cannot divide by zero!"
            else:
                return str(num1 / num2)
    return None

# --------------- GUI FUNCTIONS ---------------
def send_message():
    """
    Handle sending of messages by:
    1. Checking for arithmetic pattern.
    2. If not arithmetic, proceed with intent prediction.
    """
    message = entry.get()
    if message.strip():
        # First check if it's an arithmetic expression
        arithmetic_result = check_arithmetic(message)
        if arithmetic_result is not None:
            # It's arithmetic, so just print the result
            chat_history.insert(tk.END, f"You: {message}\n", "user")
            # Depending on pink_mode, print name as "UwUBot" or "Bot"
            bot_name = "UwUBot" if pink_mode else "Bot"
            chat_history.insert(tk.END, f"{bot_name}: {arithmetic_result}\n", "bot")
        else:
            # Otherwise, use the model's prediction
            intents_list = predict_class(message)
            result = get_response(intents_list, intents)
            chat_history.insert(tk.END, f"You: {message}\n", "user")
            bot_name = "UwUBot" if pink_mode else "Bot"
            chat_history.insert(tk.END, f"{bot_name}: {result}\n", "bot")
        entry.delete(0, tk.END)

def save_conversation():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", 
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(chat_history.get(1.0, tk.END))

# Modify send_message to work with the "ENTER" key
def on_enter_key(event):
    """
    Trigger send_message when the ENTER key is pressed.
    """
    send_message()

# Toggle state
pink_mode = False
bg_label = None
normal_title = "Chatbot"

def toggle_theme():
    """
    Toggle between normal theme and pink "UwU" theme.
    """
    global pink_mode, bg_label

    if not pink_mode:
        # --- Switch to Pink/UwU theme ---
        window.title("UwUBot")
        
        # Create an image label for the background
        global pink_bg
        pink_bg = tk.PhotoImage(file="cute_background.png")
        bg_label = tk.Label(window, image=pink_bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Lower the background label to ensure it stays at the back
        bg_label.lower()

        # Change chat text area to light pink
        chat_history.config(bg="light pink")
        chat_history.tag_config("bot", foreground="dark magenta")

        # Change frame and button colors to match the theme
        chat_frame.config(bg="light pink")
        input_frame.config(bg="light pink")
        button_frame.config(bg="light pink")
        
        send_button.config(bg="#ffe6ff", fg="black")
        save_button.config(bg="#ffe6ff", fg="black")
        toggle_theme_button.config(bg="#ffe6ff", fg="black")

        # Change input box background
        entry.config(bg="#ffe6ff")

        pink_mode = True
    else:
        # --- Revert to Normal theme ---
        window.title(normal_title)

        # Remove the background image (destroy the label or place it off-screen)
        if bg_label:
            bg_label.destroy()
            bg_label = None

        # Revert chat text area color
        chat_history.config(bg="white")
        chat_history.tag_config("bot", foreground="green")

        # Revert frame and button colors
        chat_frame.config(bg="white")
        input_frame.config(bg="white")
        button_frame.config(bg="white")

        send_button.config(bg="SystemButtonFace", fg="black")
        save_button.config(bg="SystemButtonFace", fg="black")
        toggle_theme_button.config(bg="SystemButtonFace", fg="black")

        # Revert input box
        entry.config(bg="SystemWindow")

        pink_mode = False

# --------------- TIPS ---------------
def update_tips():
    """
    Periodically update the tips display with random examples from intents.
    """
    while True:
        # Choose a random tip from intents patterns
        random_tip = random.choice([pattern for intent in intents for pattern in intent["patterns"]])
        tips_display.config(state=tk.NORMAL)  # Enable editing temporarily
        tips_display.delete(1.0, tk.END)  # Clear existing tip
        tips_display.insert(tk.END, f"You can ask: {random_tip}")  # Insert new tip
        tips_display.config(state=tk.DISABLED)  # Disable editing
        time.sleep(5)  # Wait 5 seconds before updating again

# --------------- BUILD THE GUI ---------------
window = tk.Tk()
window.title(normal_title)
window.geometry("600x700")
window.minsize(400, 500)

# Chat frame setup
chat_frame = tk.Frame(window, bg="white")
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

chat_history = tk.Text(chat_frame, wrap=tk.WORD, font=("Helvetica", 12))
chat_history.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

chat_scroll = tk.Scrollbar(chat_frame, command=chat_history.yview)
chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
chat_history['yscrollcommand'] = chat_scroll.set

# Tag configurations for user/bot text
chat_history.tag_config("user", foreground="blue", font=("Helvetica", 12, "bold"))
chat_history.tag_config("bot", foreground="green", font=("Helvetica", 12, "italic"))

# Input frame setup
input_frame = tk.Frame(window, bg="white")
input_frame.pack(fill=tk.X, padx=10, pady=5)

entry = tk.Entry(input_frame, width=50, font=("Helvetica", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
entry.bind("<Return>", on_enter_key)  # Bind the ENTER key to send_message

send_button = tk.Button(input_frame, text="Send", command=send_message, bg="SystemButtonFace")
send_button.pack(side=tk.LEFT, padx=5)

# Button frame for save and toggle theme buttons
button_frame = tk.Frame(window, bg="white")
button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

toggle_theme_button = tk.Button(button_frame, text="Toggle Theme", command=toggle_theme, bg="SystemButtonFace")
toggle_theme_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save Conversation", command=save_conversation, bg="SystemButtonFace")
save_button.pack(side=tk.RIGHT, padx=5)

# "TIPS" display area
tips_frame = tk.Frame(window, bg="white")
tips_frame.pack(fill=tk.X, padx=10, pady=5)

tips_display = tk.Text(tips_frame, wrap=tk.WORD, height=1, font=("Helvetica", 12), state=tk.DISABLED, bg="light yellow")
tips_display.pack(fill=tk.X, padx=5, pady=5)

# Start the thread to update tips
thread = threading.Thread(target=update_tips, daemon=True)
thread.start()

# Start the main loop
window.mainloop()