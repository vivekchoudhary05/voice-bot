import google.generativeai as genai
import os
import re
import speech_recognition as sr
import pyttsx3
import fitz  # PyMuPDF for PDF extraction
from dotenv import load_dotenv
from collections import deque

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro-002")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

# For demo i have used my resume text from a PDF file
resume_path = r"C:\Users\vivek\OneDrive\Desktop\voice-bot\VIVEK_CHOUDHARY_RESUME.pdf" 
resume_text = extract_text_from_pdf(resume_path)

# Defining chatbot personality with custom instructions and resume data (mainly to answer about me and like me)
system_prompt = f"""
You are Vivek Choudhary, a Machine Learning Engineer. When asked about yourself, your responses must:
- Be concise and to the point.
- Stay professional yet casual.
- Focus on efficiency, avoiding unnecessary elaboration.
- Use structured bullet points where applicable.

When asked about anything else, provide an appropriately detailed and contextual response.

### Resume Details:
{resume_text}

Keep responses aligned with your expertise and past projects.
"""

# Memory to store only the last 5 user questions 
chat_history = deque(maxlen=5)

# Initialize text-to-speech engine and speed rate
engine = pyttsx3.init()
engine.setProperty("rate", 190)  

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return None
    except sr.RequestError:
        print("Error with the speech recognition service.")
        return None

# Function to chat with Gemini (only remembers questions, prevents repetition)
def chat_with_gemini(user_input):
    # Store only the last 5 questions, not responses
    chat_history.append(user_input)

    # Format history as just questions
    history_context = "\n".join(chat_history)

    # Ensure the latest user input is not duplicated
    full_prompt = f"{system_prompt}\n\nPrevious Questions:\n{history_context}\n\nNew Question: {user_input}\nYou:"

    # Get response from Gemini
    response = model.generate_content(full_prompt)
    bot_reply = response.text.strip() if response else "No response received."
    bot_reply = re.sub(r'\*', '', bot_reply)
    return bot_reply

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main loop for voice interaction
if __name__ == "__main__":
    print("Voice-Enabled Gemini Chatbot is running... (Say 'exit' to quit)\n")
    while True:
        user_input = recognize_speech()
        if user_input:
            if "exit" in user_input.lower():
                print("Chatbot: Goodbye!")
                speak("Goodbye!")
                break
            bot_response = chat_with_gemini(user_input)
            print("Chatbot:", bot_response)
            speak(bot_response)
