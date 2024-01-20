import audioop
import pyttsx3
import datetime
import speech_recognition as sr
import  wikipedia 
import webbrowser
import os

engine =pyttsx3.init('sapi5')
voices =engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voices', voices[1].id)
  

def speak (audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour =int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning, Meg !")
    elif hour >=12 and hour<18:
        speak("Good afternoon , Meg! ")
    else:
        speak("Good evening, Meg!")
    speak("I am FRIDAY , your assistant for this personal computer .Tell me something you need !")
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
         print("listening...")
         r.pause_treshold = 1
         audio=r.listen(source)
      
    try:
        print('recoginising ....') 
        query=r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)  
        print("say that again please ...")
        return"none"
    return query

      
if __name__=="__main__" :
     wishMe()
     
     while True:
            query= takeCommand().lower()
            if 'wikipedia' in query:
                speak('searching wikipedia....')
                query = query.replace('wikipedia' , "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                
                speak(results)
                
            elif'open youtube' in  query:
                webbrowser.open("youtube.com")
            elif 'open spotify' in query:
                
                webbrowser.open("spotify.com")
            
            elif 'play a random video'in query:
                webbrowser.open("https://youtu.be/jzm2ZB8sQTQ")

        
            elif 'play my favourite song' in query:
                webbrowser.open('https://youtu.be/orJSJGHjBLI')
            