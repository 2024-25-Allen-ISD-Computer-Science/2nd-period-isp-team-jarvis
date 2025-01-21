import pyttsx3
import speech_recognition as sr
import openai
import random
import spacy
import json
from datetime import datetime
import os
import google.generativeai as genai

r_audio = sr.Recognizer()
r_audio.energy_threshold = 4000
r_audio.dynamic_energy_threshold = True

tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 200)
tts_engine.setProperty("volume", 1.0)

nlp = spacy.load("en_core_web_sm")

# -- NEED TO CHANGE TO GEMINI - need to change the functions and the main logic as well to use the new API
openai.api_key = "SECRET"

# global vars
data = {
    "to_do_list": [],
    "context": {
        "name": None,
        "location": None,
        "preferences": [],
        "last_query": None
    }
}

# loads context
CONTEXT_FILE = "context.json"
    
def load_context():
    global data
    try:
        if os.path.exists("context.json"):
            with open(CONTEXT_FILE, "r") as file:
                data["context"] = json.load(file)
    except json.JSONDecodeError:
        print("Error loading context file. Starting fresh.")
        data["context"] = {
            "name": None,
            "location": None,
            "preferences": [],
            "last_query": None
        }
              

# saves context to file
def save_context():
    with open(CONTEXT_FILE, "w") as file:
        json.dump(data["context"], file, indent=4)

# Functions
def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Capture audio input from the user."""
    with sr.Microphone as source:
        print("Listening...")
        audio = r_audio.listen(source, timeout=5, phrase_time_limit=8)
    try:
        query = r_audio.recognize_google(audio, language="en-US")
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        speak("I'm sorry, I couldn't understand you.")
        return ""
    except sr.RequestError:
        print("Error with Google API")
        speak("I'm sorry, due to technical issues, I can't respond right now.")
        return ""
    except sr.WaitTimeoutError:
        print("No speech detected within the timeout period.")
        return ""

def gpt_search(query):
    """Send the query to OpenAI GPT for processing."""
    try:
        speak("Let me check that for you...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Error:", e)
        return "I'm sorry, I couldn't fetch an answer right now."

def dynamic_greeting():
    """Generate a greeting based on the time of day."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning! How can I assist you today?"
    elif current_hour < 18:
        return "Good afternoon! What can I do for you?"
    else:
        return "Good evening! What can I help you with?"


def dynamic_response(phrase_type):
    """ Generates a random dynamic reponse"""
    responses = {
        "greeting" : ["Hi, there!", "Hello!", "Hey!", "Hey, good to see you back!"],
        "acknowledge" : ["Got it!", "Sure thing!", "Understood!", "Alright!"],
        "ask_followup" : ["Is there anything else I can help with?", "Would you like to know more?", "What else can I assist you with?"]
    }
    return random.choice(responses.get(phrase_type, [""]))

def manage_todo(query):
    """Handles to-do list with better clarity and error handling."""
    
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

def process_query(query):
    """Process the user query and handle commands."""
    global to_do_list

    # Handles To-Do List Commands
    if any(keyword in query.lower() for keyword in ["to-do", "task", "list"]):
        return manage_todo(query)

    # Checks for specific commands
    if "time" in query.lower():
        speak("Fetching the current time...")
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    elif "date" in query.lower():
        speak("Fetching today's date...")
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."
    elif "your name" in query.lower():
        speak("I am Jarvis, your virtual assistant.")
        return "I am Jarvis, your virtual assistant."
    elif "how are you" in query.lower():
        return "I'm doing great, thanks for asking!"
    elif "name" in query.lower():
        speak("What’s your name?")
        context["name"] = listen()
        return f"Nice to meet you, {context['name']}!"
    elif "location" in query.lower():
        speak("Where are you located?")
        context["location"] = listen()
        return f"Got it! You're located in {context['location']}."
    else:
        return gpt_search(query)

def jarvis_main():
    """Main function to run the virtual assistant."""
    print("Jarvis is running... Say 'exit' to stop.")
    load_context() 
    speak(dynamic_greeting()) 

    while True:
        query = listen()
        if query:
            if "exit" in query.lower():
                save_context()  
                speak("Goodbye! Take care.")
                break

            
            response = process_query(query)
            print("Jarvis:", response)
            speak(response)
            
            # Follow-up questions based on context
            if "weather" in query.lower() or "time" in query.lower():
                follow_up = dynamic_response("ask_followup")
                print(f"Jarvis: {follow_up}")
                speak(follow_up)

            context["last_query"] = query

            if "more" in query.lower() or "tell me more" in query.lower():
                if context["last_query"]:
                    response = gpt_search(context["last_query"])
                    print("Jarvis:", response)
                    speak(response)

# Run the assistant
if __name__ == "__main__":
    jarvis_main()