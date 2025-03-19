import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import time
import requests
import smtplib
import os
import openai
import pandas as pd
from bs4 import BeautifulSoup
import pywhatkit
import yfinance as yf
from tmdbv3api import TMDb, Movie, TV
import pywhatkit
from googletrans import Translator


def chat_with_ai():
    """Have a conversation with OpenAI's GPT model."""
    speak("What do you want to ask me?")
    question = listen()
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    
    answer = response["choices"][0]["message"]["content"]
    speak(answer)

def generate_ai_image():
    """Generate an AI image using DALL·E."""
    speak("What image do you want to create?")
    prompt = listen()
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = response["data"][0]["url"]
    speak(f"Here is your AI-generated image: {image_url}")

translator = Translator()

def translate_text():
    """Translate text into another language."""
    speak("What would you like to translate?")
    text = listen()
    
    speak("Which language should I translate to?")
    language = listen().lower()
    
    language_codes = {
        "spanish": "es", "french": "fr", "german": "de",
        "chinese": "zh-cn", "hindi": "hi", "arabic": "ar"
    }
    
    if language in language_codes:
        translated_text = translator.translate(text, dest=language_codes[language])
        speak(f"In {language}, you would say: {translated_text.text}")
    else:
        speak("Sorry, I don't support that language yet.")

def play_music():
    """Play music on YouTube."""
    speak("What song would you like to play?")
    song = listen()
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)

recognizer = sr.Recognizer()
engine = pyttsx3.init()
openai.api_key = "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"



tmdb = TMDb()
tmdb.api_key = "your_tmdb_api_key"

movie = Movie()
tv = TV()

def suggest_movie():
    """Suggest a movie based on genre."""
    speak("What genre are you interested in?")
    genre = listen().lower()
    
    genres_dict = {
        "action": 28, "comedy": 35, "drama": 18, "horror": 27, "sci-fi": 878
    }
    
    if genre in genres_dict:
        movies = movie.discover({"with_genres": genres_dict[genre]})
        speak(f"Here are some {genre} movies: {movies[0]['title']}, {movies[1]['title']}, {movies[2]['title']}")
    else:
        speak("I don't have recommendations for that genre.")

def suggest_tv_show():
    """Suggest popular TV shows."""
    shows = tv.popular()
    speak(f"Here are some popular TV shows: {shows[0]['name']}, {shows[1]['name']}, {shows[2]['name']}")

def get_crypto_price():
    """Fetch cryptocurrency prices."""
    speak("Which cryptocurrency do you want to check?")
    crypto = listen().lower()
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url).json()
    
    if crypto in response:
        price = response[crypto]["usd"]
        speak(f"The current price of {crypto} is {price} dollars.")
    else:
        speak("Sorry, I couldn't find the cryptocurrency price.")

def get_stock_price():
    """Fetch stock prices."""
    speak("Which company's stock price do you want to check?")
    company = listen().upper()
    
    try:
        stock = yf.Ticker(company)
        price = stock.history(period="1d")["Close"].iloc[-1]
        speak(f"The current price of {company} is {price:.2f} dollars.")
    except Exception as e:
        speak("Sorry, I couldn't find the stock price.")


def send_whatsapp_message():
    """Send a WhatsApp message via voice command."""
    speak("Who should I message?")
    phone_number = listen()
    
    speak("What should I say?")
    message = listen()
    
    pywhatkit.sendwhatmsg_instantly(f"+{phone_number}", message)
    speak("WhatsApp message sent.")

def get_latest_news():
    """Fetch latest news headlines."""
    url = "https://news.google.com/news/rss"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    headlines = soup.find_all("title")[1:6]  # First is title of Google News itself

    speak("Here are the latest news headlines:")
    for news in headlines:
        speak(news.text)

def file_manager(command):
    """Handle file operations based on voice commands."""
    if "create file" in command:
        speak("What should be the file name?")
        file_name = listen()
        with open(file_name + ".txt", "w") as f:
            speak(f"{file_name} has been created.")
    
    elif "delete file" in command:
        speak("Which file do you want to delete?")
        file_name = listen()
        if os.path.exists(file_name + ".txt"):
            os.remove(file_name + ".txt")
            speak(f"{file_name} has been deleted.")
        else:
            speak("File not found.")
    
    elif "create folder" in command:
        speak("What should be the folder name?")
        folder_name = listen()
        os.makedirs(folder_name, exist_ok=True)
        speak(f"Folder {folder_name} has been created.")
    
    elif "delete folder" in command:
        speak("Which folder do you want to delete?")
        folder_name = listen()
        if os.path.exists(folder_name):
            os.rmdir(folder_name)
            speak(f"Folder {folder_name} has been deleted.")
        else:
            speak("Folder not found.")

def send_email():
    """Send an email using Gmail SMTP."""
    speak("Who do you want to send the email to?")
    recipient = listen()
    
    # Replace this with a real email mapping
    email_dict = {
        "cherex": "chereto@example.com"
        
    }
    
    if recipient in email_dict:
        receiver_email = email_dict[recipient]
    else:
        speak("I don't have that email saved. Please provide an email address.")
        receiver_email = listen()
    
    speak("What is the subject?")
    subject = listen()
    
    speak("What is the message?")
    message = listen()
    
    sender_email = "cherinetwoyesa55@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Use an App Password if 2FA is enabled
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, email_message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(f"Error: {e}")
        def chat_with_ai():
                    """Interact with OpenAI for AI-powered conversations."""
    speak("What do you want to ask me?")
    user_query = listen()
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_query}]
        )
        answer = response["choices"][0]["message"]["content"]
        speak(answer)
    except Exception as e:
        speak("Sorry, I couldn't process your request.")
        print(f"Error: {e}")
def set_reminder():
    """Ask for the reminder details and set it."""
    speak("What should I remind you about?")
    reminder_text = listen()
    speak("In how many seconds should I remind you?")
    
    try:
        delay = int(listen())  # Convert speech to number
        speak(f"Reminder set for {delay} seconds. I will remind you.")
        time.sleep(delay)
        speak(f"Reminder: {reminder_text}")
    except ValueError:
        speak("Sorry, I couldn't understand the time. Try again.")

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input from the microphone and return text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            print("Speech service is unavailable.")
            return ""

def open_website(site_name):
    """Open a website based on user command."""
    urls = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com"
    }
    if site_name in urls:
        speak(f"Opening {site_name}")
        webbrowser.open(urls[site_name])
    else:
        speak("Sorry, I don't know that website.")

def tell_time():
    """Tell the current time."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")


def get_weather():
    """Fetch weather details for a city."""
    speak("Which city’s weather do you want to check?")
    city = listen()
    
    api_key = "7843534785359835547543"  # Replace with your OpenWeatherMap API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data.get("main"):
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't get the weather information.")
def control_system(command):
    """Shutdown, restart, or sleep the system based on voice command."""
    if "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")  # Windows Shutdown
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")  # Windows Restart
    elif "sleep" in command:
        speak("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
def open_application(command):
    """Open common applications based on voice commands."""
    if "notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad")
    elif "calculator" in command:
        speak("Opening Calculator.")
        os.system("calc")
    elif "news update" in command or "latest news" in command:
          get_latest_news()
   
    elif "browser" in command:
        speak("Opening your default browser.")
        os.system("start chrome")  # Use "start firefox" for Firefox


expense_file = "expenses.csv"

def track_expense():
    """Track expenses and save to a CSV file."""
    speak("What was the expense for?")
    category = listen()
    
    speak("How much was it?")
    amount = listen()
    
    df = pd.DataFrame([[category, amount]], columns=["Category", "Amount"])
    
    if os.path.exists(expense_file):
        df.to_csv(expense_file, mode='a', header=False, index=False)
    else:
        df.to_csv(expense_file, index=False)
    
    speak(f"Recorded an expense of {amount} for {category}.")


def search_wikipedia(query):
    """Search Wikipedia and return a summary."""
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any results for that.")

if __name__ == "__main__":
    speak("Hello! I am your personal assistant. How can I help you?")
    
    while True:
        command = listen()
        
        if "open google" in command:
            open_website("google")
        elif "open youtube" in command:
            open_website("youtube")
        elif "open github" in command:
            open_website("github")
        elif "time" in command:
            tell_time()
        elif "set a reminder" in command:
           set_reminder()
        elif "check the weather" in command:
            get_weather()
        elif "send an email" in command:
            send_email()
        elif "shutdown" in command or "restart" in command or "sleep" in command:
                       control_system(command)
        elif "open notepad" in command or "open calculator" in command or "open browser" in command:
                     open_application(command)
        elif "file" in command or "folder" in command:
                     file_manager(command)
        elif "generate image" in command or "create AI image" in command:
                        generate_ai_image()

        elif "track expense" in command or "add expense" in command:
                      track_expense()
        elif "send whatsapp" in command or "message on whatsapp" in command:
                  send_whatsapp_message()
        elif "stock price" in command:
                  get_stock_price()
        elif "crypto price" in command:
                   get_crypto_price()
        elif "suggest a movie" in command or "movie recommendation" in command:
                    suggest_movie()
        elif "suggest a TV show" in command or "TV show recommendation" in command:
                        suggest_tv_show()
        elif "play music" in command or "play song" in command:
                        play_music()
        elif "translate" in command:
                        translate_text()
        elif "talk to AI" in command or "ask a question" in command:
                    chat_with_ai()

        elif "search wikipedia" in command:
            speak("What should I search for?")
            query = listen()
            search_wikipedia(query)
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand. Please try again.")
     


