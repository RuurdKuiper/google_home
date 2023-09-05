import speech_recognition as sr
from gtts import gTTS
import os
import openai
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext
import pyttsx3
import pygame
import time


# Set your OpenAI API key here
openai.api_key = "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"

class VoiceAssistantApp:
    from process_audio import process_audio
    from output_text import display_text
    
    def __init__(self, root):

        # Initialize pygame mixer
        pygame.init()
        pygame.mixer.init()

        self.root = root
        self.root.title("Voice Assistant")
        
        self.output_label = tk.Label(root, text="Assistant:")
        self.output_label.pack()
        
        # Use a scrolledtext widget for variable-length text
        self.output_text = scrolledtext.ScrolledText(root, width=100, height=30, state="disabled")
        self.output_text.pack()
        
        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_button.pack()
        
        self.quit_button = tk.Button(root, text="Quit", command=self.root.quit)
        self.quit_button.pack()
        
        self.recognizer = sr.Recognizer()
        self.audio_thread = None

    def start_listening(self):
        self.display_text("Listening... Say something!\n\n")
        self.start_button.config(state="disabled")
        
        self.audio_thread = Thread(target=self.process_audio)
        self.audio_thread.start()

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" as well
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100  # Adjust this for response length
        )
        return response.choices[0].message.content.strip()

    def text_to_speech(self, text):
        # Check if the pygame music player is currently playing
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        time.sleep(0.5)

        # Explicitly quit the pygame mixer to release resources
        pygame.mixer.quit()

        tts = gTTS(text, tld="co.za", lang="en", slow=False)
        tts.save("response.mp3")
        time.sleep(0.5)
                   
        pygame.mixer.init()  # Initialize the pygame mixer again
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
