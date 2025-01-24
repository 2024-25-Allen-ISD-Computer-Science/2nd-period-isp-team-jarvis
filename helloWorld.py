import pyttsx3
import speech_recognition as sr
import openai
import random
import spacy
import json
from datetime import datetime
import os

r_audio = sr.Recognizer()
r_audio.energy_threshold = 4000
r_audio.dynamic_energy_threshold = True

tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 175)
tts_engine.setProperty("volume", 1.0)

nlp = spacy.load("en_core_web_sm")

# Replace with your actual OpenAI API key
openai.api_key = "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"

# Global variables using a dictionary for better organization
data = {
    "to_do_list": [],
    "context": {
        "name": None,
        "location": None,
        "preferences": [],
        "last_query": None,
    },
}

# Context Management
CONTEXT_FILE = "context.json"

def load_context():
    """Loads context from a JSON file."""
    global data
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "r") as file:
                data["context"] = json.load(file)
    except json.JSONDecodeError:
        print("Error decoding JSON from context file. Using default context.")
        data["context"] = {
            "name": None,
            "location": None,
            "preferences": [],
            "last_query": None
        }

def save_context():
    """Saves the current context to a JSON file."""
    with open(CONTEXT_FILE, "w") as file:
        json.dump(data["context"], file, indent=4)

# Speech-to-Text and Text-to-Speech
def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Capture audio input from the user and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r_audio.listen(source, phrase_time_limit=8)
    try:
        query = r_audio.recognize_google(audio, language="en-US")
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        print("Error with the Google API")
        speak("Sorry, there was an error with the Google API.")
        return ""
    except sr.WaitTimeoutError:
        print("No speech detected within the timeout period.")
        return ""

# Enhanced Response Generation
def jarvis_search(query):
    """Send the query to OpenAI jarvis for processing with improved error handling."""
    try:
        speak("Let me check that for you...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change the model if needed
            messages=[
                {"role": "system", "content": "You are jarvis, a helpful assistant."},
                {"role": "user", "content": query},
            ],
            max_tokens=150,  # Increased max_tokens for more detailed responses
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return "I'm sorry, I encountered an issue with the OpenAI API. Please try again later."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "I'm sorry, I couldn't fetch an answer right now due to an unexpected error."

# Dynamic Responses and Greetings
def dynamic_greeting():
    """Generate a time-based greeting."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def dynamic_response(phrase_type):
    """Generate a random dynamic response."""
    responses = {
        "greeting": ["Hi there!", "Hello!", "Hey, how's it going?"],
        "acknowledge": ["Sure!", "Got it!", "Okay!", "Alright!"],
        "ask_followup": [
            "Would you like to know more?",
            "Anything else I can help with?",
            "Need further assistance?",
        ],
    }
    return random.choice(responses.get(phrase_type, [""]))

# To-Do List Management
def manage_todo(query):
    """Handle to-do list operations with improved clarity and error handling."""
    
    if "add" in query:
        speak("What task would you like to add?")
        task = listen()
        if task:
            data["to_do_list"].append(task)
            return f"Task '{task}' added."
        else:
            return "Task not added. I didn't catch the task."

    elif any(word in query for word in ["show", "view", "display"]):
        if not data["to_do_list"]:
            return "Your to-do list is empty."
        tasks = "\n".join(
            [f"{i+1}. {task}" for i, task in enumerate(data["to_do_list"])]
        )
        return f"Your tasks:\n{tasks}"

    elif any(word in query for word in ["remove", "complete", "delete"]):
        if not data["to_do_list"]:
            return "Your to-do list is empty."
        speak("Which task to remove? Say the number.")
        tasks_str = "\n".join([f"{i+1}. {task}" for i, task in enumerate(data["to_do_list"])])
        speak(tasks_str)
        try:
            task_num = listen()
            task_index = int(task_num) - 1
            if 0 <= task_index < len(data["to_do_list"]):
                removed_task = data["to_do_list"].pop(task_index)
                return f"Task '{removed_task}' removed."
            else:
                return "Invalid task number."
        except ValueError:
            return "Invalid input. Please say a number."
    
    elif "clear" in query:
        data["to_do_list"].clear()
        return "To-do list cleared."

    else:
        return "I didn't understand your request for the to-do list. You can add, show, remove, or clear tasks."

# Query Processing and Command Handling
def process_query(query):
    """Process user query, handle commands, or send to jarvis."""
        
    if any(word in query for word in ["to-do", "task", "list"]):
        return manage_todo(query)

    # Keyword-based actions
    if "time" in query:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}."
    elif "date" in query:
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."
    elif "your name" in query:
        return "I am jarvis, your virtual assistant."
    elif "how are you" in query:
        return "I'm doing well, thanks for asking!"
    elif "my name" in query and data["context"]["name"]:
        return f"Your name is {data['context']['name']}."
    elif "my name" in query:
        speak("What's your name?")
        data["context"]["name"] = listen()
        if data["context"]["name"]:
            return f"Nice to meet you, {data['context']['name']}!"
        else:
            return "I didn't catch your name."
    elif "location" in query:
        speak("What's your location?")
        data["context"]["location"] = listen()
        if data["context"]["location"]:
            return f"Got it. You're in {data['context']['location']}."
        else:
            return "I didn't catch your location."
    elif "tell me more" in query and data["context"]["last_query"]:
        # Fetch additional information about the last query
        return jarvis_search(f"Tell me more about: {data['context']['last_query']}")
    else:
        return jarvis_search(query)

# Main Program Logic
def jarvis_main():
    """Main function to run the jarvis virtual assistant."""
    print("jarvis is running... Say 'bye' to stop.")
    load_context()
    speak(f"{dynamic_greeting()} I'm jarvis. How can I help you?")

    while True:
        query = listen()
        if not query:
            continue

        if "bye" in query:
            speak("Goodbye! Have a great day.")
            save_context()
            break   

        response = process_query(query)
        print(f"jarvis: {response}")
        speak(response)

        # Offer follow-up for specific queries
        if any(word in query for word in ["weather", "time"]):
            follow_up = dynamic_response("ask_followup")
            print(f"jarvis: {follow_up}")
            speak(follow_up)

        data["context"]["last_query"] = query

# Run the assistant
if __name__ == "__main__":
    jarvis_main()