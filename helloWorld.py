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
def load_context():
    global context
    if os.path.exists("context.json"):
        with open("context.json", "r") as file:
            context = json.load(file)

# saves context to file
def save_context():
    with open("context.json", "w") as file:
        json.dump(context, file)

# Functions
def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Capture audio input from the user."""
    with sr.Microphone() as source:
        r_audio.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = r_audio.listen(source)
        try:
            query = r_audio.recognize_google(audio, language='en-US')
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            print("Error with the Google API")
            speak("Sorry, there was an error with the Google API.")
            return None

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
    """Generate random dynamic responses based on the context."""
    if phrase_type == "greeting":
        greetings = ["Hi there!", "Hello!", "Hey, how’s it going?"]
        return random.choice(greetings)
    elif phrase_type == "acknowledge":
        acknowledgments = ["Sure!", "Got it!", "Okay!"]
        return random.choice(acknowledgments)
    elif phrase_type == "ask_followup":
        follow_up_questions = [
            "Would you like to know more about that?",
            "Do you need anything else?",
            "Is there anything else I can help with?"
        ]
        return random.choice(follow_up_questions)

def manage_todo(query):
    """Handle the to-do list actions based on user query."""
    global to_do_list

    if "add" in query .lower():
        speak("What task would you like to add?")
        task = listen()
        if task:
            to_do_list.append(task)
            return f"Task '{task}' added to your to-do list."
        else:
            return "I couldn't hear the task clearly. Please try again."

    elif "show" in query.lower() or "view" in query.lower():
        if not to_do_list:
            return "Your to-do list is currently empty."
        tasks = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(to_do_list)])
        return f"Here are your tasks:\n{tasks}"

    elif "remove" in query.lower() or "complete" in query.lower():
        if not to_do_list:
            return "Your to-do list is empty. There's nothing to remove."
        speak("Which task would you like to remove? Please say the number.")
        tasks = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(to_do_list)])
        speak(f"Here are your tasks:\n{tasks}")
        task_number = listen()
        try:
            task_index = int(task_number) - 1
            if 0 <= task_index < len(to_do_list):
                removed_task = to_do_list.pop(task_index)
                return f"Task '{removed_task}' removed from your to-do list."
            else:
                return "That task number is not valid."
        except ValueError:
            return "I couldn't understand the task number. Please try again."

    elif "clear" in query.lower():
        to_do_list.clear()
        return "Your to-do list has been cleared."

    else:
        return "I didn't understand your request regarding the to-do list. Please try saying add, show, remove, or clear."

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