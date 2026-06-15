import pyttsx3
import webbrowser
import speech_recognition as sr
import time
import music_lib
import ai
import wikipedia
import subprocess
import random
import requests
import os
import keyboard
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

r = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)

def get_weather(city):
    key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    data = requests.get(url).json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"{city} is {temp}°C with {desc}"

def get_news():
    key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={key}&pageSize=3"
    data = requests.get(url).json()
    headlines = [article["title"] for article in data["articles"][:3]]
    return headlines

def fxn(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open reddit" in c.lower():
        webbrowser.open("https://www.reddit.com/")
    elif "open guess who" in c.lower():
        webbrowser.open("https://shubhans-gg.github.io/Anime_guesswho/")
    elif "open cricinfo" in c.lower():
        webbrowser.open("https://www.espncricinfo.com/")

    elif "open notepad" in c.lower():
        subprocess.Popen("notepad.exe")
    elif "open calculator" in c.lower():
        subprocess.Popen("calc.exe")

    elif "flip a coin" in c.lower():
        result = random.choice(["Heads", "Tails"])
        print(f"It's {result}")
        speak(f"It's {result}")
    elif "roll a dice" in c.lower():
        result = random.randint(1, 6)
        print(f"You rolled {result}")
        speak(f"You rolled {result}")
    
    elif c.lower().startswith("calculate"):
        query = c.lower().replace("calculate", "").strip()
        query = query.replace("plus", "+")
        query = query.replace("minus", "-")
        query = query.replace("times", "*")
        query = query.replace("multiplied by", "*")
        query = query.replace("divided by", "/")
        query = query.replace("power", "**")
        try:
            result = eval(query)
            print(result)
            speak(f"The answer is {result}")
        except:
            speak("Sorry, I couldn't calculate that")

    elif "translate" in c.lower():
        query = c.lower().replace("translate", "").replace("to hindi", "").strip()
        result = GoogleTranslator(source="auto", target="hi").translate(query)
        speak(result)

    elif "weather" in c.lower():
        city = c.lower().replace("weather", "").replace("in", "").strip()
        if not city:
            city = "Fatehpur"  # default city
        result = get_weather(city)
        print(result)
        speak(result)

    elif "news" in c.lower():
        headlines = get_news()
        speak("Here are today's top headlines")
        for headline in headlines:
            print(headline)
            speak(headline)
            time.sleep(0.5)
    
    elif "wikipedia" in c.lower():
        query = c.lower().replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=3)
            print(result)
            speak(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results, please be more specific")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia for that")

    elif c.lower().startswith("search"):
        query = c.split(" ", 1)[1]
        webbrowser.open(f"https://google.com/search?q={query}")

    elif c.lower().startswith("play"):
        song=c.lower().split(" ",1)[1]
        for key in music_lib.music:
            if key.lower() == song.lower():
                webbrowser.open(music_lib.music[key])

    elif "rest" in c.lower():
        speak("As you command, Master")
        exit()

    else:
        # anything unrecognised → ask Gemini
        print("Asking Gemini...")
        response = ai.ask_gemini(c)
        print("Gemini:", response)
        speak(response)
    

if __name__=="__main__":
    speak("Initializing Shadow...")
    
    while True:
        if keyboard.is_pressed("esc"):
            speak("Goodbye Master")
            exit()
        print("recognising...")
        
        # # recognize speech using Sphinx
        # try:
        #     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        # except sr.UnknownValueError:
        #     print("Sphinx could not understand audio")
        # except sr.RequestError as e:
        #     print("Sphinx error; {0}".format(e))

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
             
            with sr.Microphone() as source:
                # r.adjust_for_ambient_noise(source)  # Without it, mic picks up background noise and recognition suffers
                print("Say something!")
                audio = r.listen(source)      #,timeout=5, phrase_time_limit=3
            word=r.recognize_google(audio)
            print(word)
            if (word.lower()=="arise"):
                speak("Yes master")
                with sr.Microphone() as source:
    
                    print("Shadow activated")
                    audio = r.listen(source)
                    try:
                        command=r.recognize_google(audio)
                        print(command)
                        fxn(command)
                    except sr.UnknownValueError:
                        speak("Sorry Master but I couldn't understand that command")
            
            elif "rest" in word.lower():
                speak("As you command, Master")
                exit()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))