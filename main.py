import speech_recognition as sr
from gtts import gTTS
import os
import openai
from dotenv import load_dotenv
load_dotenv('.env')

# Set your OpenAI API key here
openai.api_key = OPENAI_API_KEY

def capture_speech():
    recognizer = sr.Recognizer()
    matches = ['Lizard', 'lizard']

    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(text)
        if any([x in text for x in matches]):
            return text
        else:
            return None
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" as well
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100  # Adjust this for response length
    )
    return response.choices[0].message.content.strip()

def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    os.system("start " + filename)  # Play the generated audio

if __name__ == "__main__":
    print("Voice Assistant: Ready to assist!")

    while True:
        input_text = capture_speech()
        if input_text:
            print("You:", input_text)
            
            response_text = generate_response(input_text)
            print("Assistant:", response_text)
            
            text_to_speech(response_text, "response.mp3")
