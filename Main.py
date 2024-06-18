from tkinter import * 
import tkinter.font as tkFont
from PIL import Image
import Mathematics
from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
import os
import requests
from bs4 import BeautifulSoup
import datetime
import time
import psutil
import pyautogui as pg
import keyboard
from PIL import Image
import speedtest 
import webbrowser
import pyjokes
import requests
from AppOpener import open,close
import pywhatkit as kit
import wikipedia
from ChromeA import ChromeCode
from GatherImages import GatherImage,ShowGatheredImages


root = Tk() 
root.geometry('900x700')

assistant_name = 'DS'

def speak(command):
    t1 = gTTS(text=command, lang='en' , slow=False) 
    t1.save("./output.mp3")
    playsound("./output.mp3")
    os.remove('./output.mp3')

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        text.insert(END , "Listening.......\n")
        text.update_idletasks()
        print("Listening ...... ")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)

        try:
            text.insert(END,"Recongnising.......\n")
            text.update_idletasks()
            print("Recognising ... ")
            data = r.recognize_google(audio , language='en-in')
            print(f"User said : {data}")
        except Exception as e:
            # speak("Say that again ")
            return "none"
        return data

def wish():
    hour = int(datetime.datetime.now().hour)
    if(hour>=0 and hour<12):
        speak("Good Morning ")
    elif(hour<=4):
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak(f"I am {assistant_name} , How can I help you")

def get_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url) 
    
    soup = BeautifulSoup(response.text, "html.parser") 
    headlines = soup.find("body").find_all("h3") 
    unwanted = ["BBC World News TV", "BBC World Service Radio", 
                "News daily newsletter", "Mobile app", "Get in touch"] 
    
    for x in list(dict.fromkeys(headlines)): 
        if x.text.strip() not in unwanted: 
            text.insert(END , x.text.strip()+"\n")
            text.update_idletasks()
            speak(x.text.strip()) 
    

def offlineCompute():
    while True:
        command = takecommand().lower()
        text.insert(END , "User Said : " + command+"\n")
        text.update_idletasks()
        if 'exit' in command or "see you tomorrow" in command:
            speak("thank you , Have a nice day")
            text.insert(END , "Thank you \n Have a nice day")
            text.update_idletasks()
            break
        else:
            result = Mathematics.offline(command)
            text.insert(END , result + "\n")
            text.update_idletasks()
            speak(result)

def online():
    wish()
    while True:
        command = takecommand().lower()
        text.insert(END , "User Said : " + command+"\n")
        text.update_idletasks()
        try:
            if 'time' in command:
                hour = datetime.datetime.now().hour
                min = datetime.datetime.now().minute
                speak("Time is : ")
                speak(f"{hour} hours and {min} minutes")
                text.insert(END , f"Time is {hour} hours and {min} minutes")
            elif 'battery percentage' in command:
                battery = psutil.sensors_battery()
                if battery is None:
                    text.insert(END , "No battery found.")
                    text.update_idletasks()
                    speak("Battery not found")
                else:
                    percentage = battery.percent
                    text(END , f"Battery Percentage: {percentage}%")
                    text.update_idletasks()
                    speak(f"Battery Percentage: {percentage}%")
            elif "mute" in command:
                speak("volume muted")
                pg.press("volumemute")
            elif "unmute" in command:
                speak("volume unmuted")
                pg.press("volumemute")
            elif "decrease volume" in command or "volume down" in command or "down the volume" in command or "decrease the volume" in command:
                speak("volume decreased by 10 %")
                for i in range(5):
                    pg.press("volumedown")
            elif "increase volume" in command or "volume up" in command or "increse the volume" in command:
                speak("volume increased by 10 %")
                for i in range(5):
                    pg.press("volumeup")
            elif "open notification" in command:
                speak("Opening notification panel")
                keyboard.press_and_release("windows+n")
            elif "close notification" in command:
                speak("closing notification panel")
                keyboard.press_and_release("windows+n")
            elif "screenshot" in command:
                if "take" in command:
                    img = pg.screenshot()
                    img.save(f"./images/ssphoto.png")
                elif "show" in command or "open" in command:
                    img = Image.open("./images/ssphoto.png")
                    img.show()
            elif "switch" in command:
                keyboard.press_and_release("alt+tab")
            elif "internet speed" in command:
                speak("testing started")
                speed = speedtest.Speedtest(secure=1)
                speak("Loading server list...")
                speed.get_servers()
                speak("Choosing best server...")
                best = speed.get_best_server()
                print("tesing started")
                speak("please wait a minute for accurate testing")
                try:
                    upload_speed = speed.upload() / 1048576
                    download_speed = speed.download() / 1048576
                except Exception as e:
                    print("error occured")
                    speak("sorry error occured try again")

                print("upload speed is " , upload_speed , "mb per second")
                speak(f"upload speed is {upload_speed}mb per second")
                speak(f"download speed is {download_speed}mb per second")
                print("download speed is " , download_speed , "mb per second")
                text.insert(END , f"upload speed is {upload_speed} mb/s and Download speed is {download_speed} mb/s")
                text.update_idletasks()
            elif "where is" in command or "locate" in command:
                location = command.replace("locate","")
                location = location.replace("where is","")
                location = location.replace("in google maps","")
                location = location.strip()
                url = "https://www.google.com/maps/place/"+location
                speak(f"This the place where {location} is ")
                webbrowser.open(url)
            elif 'navigate' in command:
                command = command.replace("navigate","")
                command = command.replace("from","")
                command = command.replace("to","")
                command = command.split()
                route1 = command[0].strip()
                route2 = command[1].strip()
                speak(f"Geeting a navigation route from {route1} to {route2}")
                url = f"https://www.google.com/maps/dir/{route1}/{route2}"
                webbrowser.open(url)
            elif "joke" in command:
                joke = pyjokes.get_joke()
                speak(joke)
            elif "news" in command:
                get_news()
            elif "lock the system" in command or "lock" in command:
                keyboard.press_and_release("windows+l")
            elif "type" in command:
                command = command.replace("type","").strip()
                speak("typing"+command)
                pg.write(command , 0.1)
            elif "open" in command and 'tab' not in command and 'images' not in command:
                command = command.replace("open","").strip()
                command = command.replace("app","").strip()
                speak(f"Opening {command} ")
                text.insert(END,f"Opening {command}")
                text.update_idletasks()
                open(command , match_closest=True)      
            elif "close" in command and 'tab' not in command and 'images' not in command:
                command = command.replace("close","")
                command = command.replace("app","")
                if command=='whats':
                    command='whatsapp'        
                speak(f"closing {command}")        
                close(command , match_closest=True)
                
            elif "weather" in command or "temperature" in command:
                command = command.replace("temperature","")
                command = command.replace("weather","")
                command = command.replace("what is","")
                command = command.replace("in" , "")
                url = "https://www.google.com/search?q="+"weather"+command
                html = requests.get(url).content
                soup = BeautifulSoup(html, "html.parser")
                temp = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
                str = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
                data = str.split("\n")
                time = data[0]
                sky = data[1]
                temp = f"Temperature in {command} is {temp}"
                sky = f"Today sky is {sky}"
                speak(temp)
                speak(sky)
                text.insert(END , temp)
                text.update_idletasks()
            elif "search" in command:
                command = command.replace("search","")
                command = command.replace("in","")
                query = command.strip()
                if "google" in query:
                    query = query.replace("google","")
                    speak(f"Searching {query} in google")
                    url = f"https://www.google.com.tr/search?q={query}"
                    webbrowser.open(url)
                    text.insert(END , f"Searching {query} in google")
                    text.update_idletasks()
                elif "youtube" in query:
                    query = query.replace("youtube","")
                    speak(f"Searching {query} in youtube")
                    url = f"https://www.youtube.com/results?search_query={query}"
                    text.insert(END , f"Searching {query} in youtube")
                    text.update_idletasks()
                    webbrowser.open(url)
                elif "wikipedia" in query:
                    query = query.replace("wikipedia","")
                    speak(f"Searching {query} in wikipedia")
                    result = wikipedia.summary(query , sentences=2)
                    text.insert(END , f"Searching {query} in wikipedia")
                    text.update_idletasks()
                    speak(f"According to wikipedia , {result}")
            elif "play" in command:
                command = command.replace("play" , "")
                command = command.replace("song" , "")
                command = command.strip()
                kit.playonyt(command)
            elif "maximize window" in command:
                keyboard.press_and_release("windows+up")
            elif "minimize window" in command:
                keyboard.press_and_release("windows+down")
            elif "send" in command and "message" in command:
                command = command.replace("message","")
                command = command.replace("send","").strip()
                user = command[2:].strip()
                speak(f"what message do you want to send to {user}")
                message = takecommand()
                open("whatsapp",match_closest=True)
                time.sleep(4)
                pg.hotkey("ctrl","f")
                pg.write(user,0.1)
                time.sleep(2)
                pg.press('tab')
                pg.press('enter')
                time.sleep(1.5)
                pg.write(message,0.1)
                pg.press('enter')
                speak("Message sent successfully")
                text.insert(END,"whatsapp message sent successfully").update_idletasks()
            elif "close chat" in command:
                time.sleep(4)
                pg.hotkey("ctrl","w")
            elif "tab" in command or "tabs" in command:
                code = ChromeCode(query)
                if code != False:
                    keyboard.press_and_release(code)
                else:
                    speak("sorry , unexpected error occur , Try saying that again ")
            elif ("gather" in command or "generate" in command ) and "image" in command:
                command = command.replace("gather","")
                command = command.replace("generate","")
                command = command.replace("image" , "")
                speak(f"Gathering {command} image")
                GatherImage(command)     
                speak("Gathered Images are saved successfully in gathered images folder")               
            elif ("gathered images" in command or "saved images" in command ) and ("show" in command or "open" in command):
                ShowGatheredImages()        
            elif "movies in" in command:
                command = command.replace("show movies in","")
                command = command.strip()
                url = f'https://in.bookmyshow.com/explore/movies-{command}'
                speak(f"getting movies in {command}")
                text.insert(END , f"getting movies in {command}")
                text.update_idletasks()
                webbrowser.open(url)

            elif 'sleep' in command:
                speak("I am going for a nap , If you need help just wake me up")
                break
        except Exception as e:
            speak("error occured")


def exit():
    root.destroy()

def mainOnline():
    while True:
        permission = takecommand().lower()
        if "wake up" in permission or "get up" in permission:
            wish()
            online()
        elif "good bye" in permission or "byee" in permission or "bye" in permission or "see you later" in permission or "see you tomorrow" in permission or "talk you later" in permission:
            speak("Ok , I hope this day would be a great day for you")
            text.insert(END , "ok , I hope this day would be a great day for you")
            text.update_idletasks()
            exit()

root.title("PERSONAL VOICE ASSISTANT")
fontObj = tkFont.Font(family = "Arial",size=20,weight="bold")
fontObj1 = tkFont.Font(family = "Arial",size=16)
fontObj2 = tkFont.Font(family = "Arial",size=18)
font1 = ('times', 12, 'bold')

title = Label(root , text = "Hi , I am your Personal Voice Assistant",font=fontObj)
offlinebutton = Button(root , text = "Offline\nOperations",font=fontObj1 , command=offlineCompute)
onlinebutton = Button(root , text="Online\nOperations",font=fontObj1,command=online)
exitbutton = Button(root , text="Exit",font=fontObj2 , command=exit)
text=Text(root,height=10,width=70)

scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)



title.place(x=150,y=50)
offlinebutton.place(x=150,y=150)
onlinebutton.place(x=350,y=150)
exitbutton.place(x=550,y=155)
text.place(x=100,y=250)


root.resizable(False , False)
root.mainloop()