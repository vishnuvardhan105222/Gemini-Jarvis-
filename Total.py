import requests
import speech_recognition as sr

def mic1():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("Say something: ")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            print("You Said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""

def generate_content(query):
    # Generate content using Gemini API
    system_message=f"You are an AI bot, your name is Jarvis find the content related to query:"
    key = "AIzaSyD_iEtIx2I9aA5zjS4Z-y1MCMdsdIcftV4"  # Replace <YOUR_API_KEY> with your actual API key
    messages = [{"role": "user", "parts": [{"text": query}]}]
    data = {"contents": messages}
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + key
    response = requests.post(url, json=data)
    if response.status_code == 200:
        content = response.json().get("candidates")[0].get("content").get("parts")[0].get("text")
        print("Gemini Response:", content)
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    query = mic1()
    if query:
        generate_content(query)
