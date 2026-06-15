import pyttsx3
import webbrowser
import speech_recognition as sr
import time
import music_lib
import ai

r = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)

def fxn(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open reddit" in c.lower():
        webbrowser.open("https://www.reddit.com/")
    elif "open guess who" in c.lower():
        webbrowser.open("https://shubhans-gg.github.io/Anime_guesswho/")
    elif "open cricinfo" in c.lower():
        webbrowser.open("https://www.espncricinfo.com/")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ",1)[1]
        for key in music_lib.music:
            if key.lower() == song.lower():
                webbrowser.open(music_lib.music[key])

    else:
        # anything unrecognised → ask Gemini
        print("Asking Gemini...")
        response = ai.ask_gemini(c)
        print("Gemini:", response)
        speak(response)
    

if __name__=="__main__":
    speak("Initializing Panda...")
    while True:
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
                        speak("Sorry Master but I couldn't understand command")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))