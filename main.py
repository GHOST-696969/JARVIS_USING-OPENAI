import speech_recognition as sr
import webbrowser
import pyttsx3
from openai import OpenAI  # ✅ updated import
import threading
import os

print("Jarvis is starting...")

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set OpenAI API Key
client = OpenAI(api_key="....")  # 🔑 Replace with your actual key

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def aiProcessesCommand(command):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, an intelligent, witty virtual assistant like Siri or Alexa. Respond smartly and helpfully."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return "I'm having trouble connecting to OpenAI."

def listen_for_command(timeout=3, phrase_time_limit=4):
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        print("Recognizing...")
        return recognizer.recognize_google(audio_data)

def processCommand(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail.")
    elif "open stack overflow" in command:
        webbrowser.open("https://stackoverflow.com")
        speak("Opening Stack Overflow.")
    elif "open github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub.")
    elif "open chatgpt" in command:
        webbrowser.open("https://chat.openai.com")
        speak("Opening ChatGPT.")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web.")
    elif "open reddit" in command:
        webbrowser.open("https://www.reddit.com")
        speak("Opening Reddit.")
    elif "open amazon" in command:
        webbrowser.open("https://www.amazon.in")
        speak("Opening Amazon.")
    elif "open netflix" in command:
        webbrowser.open("https://www.netflix.com")
        speak("Opening Netflix.")
    elif "play" in command:
        query = command.replace("play", "").strip()
        speak(f"Where do you want to play {query}? YouTube or JioSaavn?")
        try:
            choice = listen_for_command(timeout=4, phrase_time_limit=4).lower()
            if "youtube" in choice:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                speak(f"Playing {query} on YouTube.")
            elif "jio" in choice or "saavn" in choice:
                webbrowser.open(f"https://www.jiosaavn.com/search/{query}")
                speak(f"Playing {query} on JioSaavn.")
            else:
                speak("I didn't catch that platform. Please say YouTube or JioSaavn.")
        except Exception as e:
            print("Error:", e)
            speak("I couldn't get your response.")
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}.")
    elif "exit" in command or "shutdown" in command:
        speak("Shutting down. Goodbye!")
        exit()
    else:
        response = aiProcessesCommand(command)
        speak(response)

def listen_and_process():
    try:
        command = listen_for_command(timeout=5, phrase_time_limit=6).lower()
        print("Command received:", command)
        processCommand(command)
    except sr.WaitTimeoutError:
        speak("I didn't catch that. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
    except Exception as e:
        print("Command error:", e)
        speak("Something went wrong.")

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        speak("Jarvis is ready.")

    while True:
        try:
            print("\nSay 'Jarvis' to activate.")
            trigger = listen_for_command(timeout=5, phrase_time_limit=4).lower()
            print("You said:", trigger)

            if "jarvis" in trigger:
                speak("Yes sir, how can I assist you?")
                listen_and_process()

        except sr.WaitTimeoutError:
            print("Waiting for wake word...")
        except sr.UnknownValueError:
            print("Wake word not recognized.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print("General error:", e)
