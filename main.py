import pyttsx3
# import edge_tts
# import asyncio
# import pygame
import webbrowser
import pywhatkit
import speech_recognition as sr
import time
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

# pygame.mixer.init()

#webbrowser.register('brave', None, webbrowser.BackgroundBrowser("C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"))

#this will check if the user has brave, if not then just stick to the default browser
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
if os.path.exists(brave_path):
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
    webbrowser.open = webbrowser.get('brave').open


#This was way slower than pyttsx3
# async def speak_async(text):
#     communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural")  
#     await communicate.save("speech.mp3")

# def speak(text):
#     # 2. Fetch the audio from the internet and save it
#     asyncio.run(speak_async(text))
    
#     # 3. Load and play the file
#     pygame.mixer.music.load("speech.mp3")
#     pygame.mixer.music.play()
    
#     # 4. Wait for it to finish speaking
#     while pygame.mixer.music.get_busy():
#         time.sleep(0.1)
        
#     # 5. Unload the file from memory so it can be overwritten safely next time
#     pygame.mixer.music.unload()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    #time.sleep(1)
    del engine  # This forces Python to instantly destroy the engine and free up the system increasing speed


def get_weather(city):
    key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    try:
        response = requests.get(url)
        # Check if the API request was successful (Status Code 200)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The weather in {city} is currently {temp} degrees Celsius with {desc}."
        elif response.status_code == 404:
            return f"Master,I wasn't able to find a city named {city}. There may be something wrong with the spelling."
        else:
            return "I'm having trouble accessing the weather service right now."
    except Exception as e:
        return f"Error fetching weather: {e}"

def get_news():
    key = os.getenv("NEWS_API_KEY")
    
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={key}&pageSize=3"
    data = requests.get(url).json()
    
    if not data["articles"]:
        return ["No news found"]
    headlines = [article["title"] for article in data["articles"][:3]]
    return headlines

def fxn(c):

    if c.lower().startswith("search"):
        query = c.split(" ", 1)[1]
        webbrowser.open(f"https://google.com/search?q={query}")

    elif "open youtube" in c.lower():
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
    

    elif "translate" in c.lower():
        query = c.lower().replace("translate", "").replace("to hindi", "").strip()
        result = GoogleTranslator(source="auto", target="hi").translate(query)
        print(f"Translation: {result}")
        speak(f"The translation is")
        webbrowser.open(f"https://translate.google.com/?sl=en&tl=hi&text={query}")


    elif "weather" in c.lower():
        city = c.lower()
        # remove all these words
        for word in ["weather", "how is the", "what is the", "today","today's", "report", "in", "at", "of"]:
            city = city.replace(word, "")
        city = city.strip()
        if not city:
            city = "Fatehpur"  # default city when no city mentioned
        print(f"Searching weather for: {city}")  
        result = get_weather(city)
        print(result)
        speak(result)

    elif "news" in c.lower():
        headlines = get_news()
        if headlines == ["No news found"]:
            speak("Sorry, I couldn't fetch the news right now")
        else:
            speak("Here are today's top headlines")
            for i, headline in enumerate(headlines):
                print(f"Headline {i+1}: {headline}")
                try:
                    clean = headline.encode("ascii", "ignore").decode()
                    
                    speak(clean)
                except:
                    print(f"Couldn't speak headline {i+1}")
                time.sleep(0.5)
    
    elif "wikipedia" in c.lower():
        query = c.lower().replace("wikipedia", "").strip()
        try:
            wikipedia.set_user_agent("Shadow/1.0")
            result = wikipedia.summary(query, sentences=3)
            print(result)
            speak(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results, please be more specific")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia for that")

    

    elif c.lower().startswith("play"):
        song=c.lower().split(" ",1)[1]
        print(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)
    #     for key in music_lib.music:
    #         if key.lower() == song.lower():
    #             webbrowser.get('brave').open(music_lib.music[key])

    elif "rest" in c.lower().split():
        speak("As you command, Master")
        exit()

    else:
        # anything unrecognised → ask Gemini
        print("Asking Gemini...")
        response = ai.ask_gemini(c)
        if str(response).startswith("Error:"):
            print(f"Gemini API Error: {response}")
            speak("Master, other people requests have surrounded me, I'll be at your command very soon")
        else:
    
            print("Gemini:", response)
            speak(response)

if __name__=="__main__":
    speak("Initializing Shadow...")
    with sr.Microphone() as source:
        print("Calibrating background noise...")
    
        r.adjust_for_ambient_noise(source, duration=1) 
        speak("Shadow is online.")
    
        while True:

            if keyboard.is_pressed("esc"):
                speak("Sorry Master")
                exit()
            
            print("\nWaiting for wake word...")
            
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
                
                    # r.adjust_for_ambient_noise(source)  # Without it, mic picks up background noise and recognition suffers
                    audio = r.listen(source, timeout=None, phrase_time_limit=3)
                    word = r.recognize_google(audio).lower()
                    print(word)

                    if (word.lower()=="arise"):
                        speak("Yes master")
                        print("Shadow activated")
                        
                        try:
                            command_audio = r.listen(source, timeout=5, phrase_time_limit=8)
                            command = r.recognize_google(command_audio)
                            print(command)

                            fxn(command)

                        except sr.UnknownValueError:
                            speak("Sorry Master but I couldn't understand that command")
                        except sr.WaitTimeoutError:
                            print("Didn't hear a command. Going to sleep.")
                    
                    if "rest" in word.lower().split():
                        speak("As you command, Master")
                        exit()

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                pass
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))