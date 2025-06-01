import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox, Style
from gtts import gTTS
import os
import speech_recognition as sr
from translate import Translator

LANGUAGES = [
    ('English', 'en'),
    ('Hindi', 'hi'),
    ('Gujarati', 'gu'),
    ('Marathi', 'mr'),
    ('Telugu', 'te'),
    ('Tamil', 'ta'),
    ('Bengali', 'bn'),
    ('Kannada', 'kn'),
    ('Malayalam', 'ml'),
    ('Punjabi', 'pa'),
    ('Urdu', 'ur'),
    ('Spanish', 'es'),
    ('French', 'fr'),
    ('German', 'de'),
    ('Italian', 'it'),
    ('Russian', 'ru'),
    ('Chinese', 'zh'),
    ('Japanese', 'ja'),
    ('Arabic', 'ar'),
    ('Portuguese', 'pt'),
]

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def show_main_menu():
    clear_window()
    top_frame = Frame(root, bg="#2E4053", width=900, height=100)
    top_frame.place(x=0, y=0)
    Label(top_frame, text="🎤 TEXT-SPEECH Translator", font=("Segoe UI", 24, "bold"), bg="#2E4053", fg="white").place(x=200, y=30)

    Button(root, text="Text To Speech", width=20, font=("Segoe UI", 16), bg="#00B894", fg="white", relief=FLAT, command=text_to_speech).place(x=310, y=170)
    Button(root, text="Speech To Text", width=20, font=("Segoe UI", 16), bg="#0984E3", fg="white", relief=FLAT, command=speech_to_text).place(x=310, y=250)
    Button(root, text="Speech To Speech", width=20, font=("Segoe UI", 16), bg="#fdcb6e", fg="#2d3436", relief=FLAT, command=speech_to_speech).place(x=310, y=330)

def text_to_speech():
    def speak_now():
        text = text_area.get(1.0, END).strip()
        input_lang_display = input_lang_combobox.get()
        output_lang_display = output_lang_combobox.get()
        input_lang_code = next((code for name, code in LANGUAGES if name == input_lang_display), None)
        output_lang_code = next((code for name, code in LANGUAGES if name == output_lang_display), None)
        if text and input_lang_code and output_lang_code:
            try:
                # Translate text from input language to output language
                if input_lang_code != output_lang_code:
                    translator = Translator(from_lang=input_lang_code, to_lang=output_lang_code)
                    translated_text = translator.translate(text)
                else:
                    translated_text = text
                # Speak the translated text in output language
                tts = gTTS(translated_text, lang=output_lang_code, slow=False)
                tts.save("output.mp3")
                os.system("start output.mp3")
                show_message(f"Spoken: {translated_text}")
            except Exception as e:
                show_message(f"Error: {e}")
        else:
            show_message("Text area is empty or language not selected.")

    clear_window()
    top_frame = Frame(root, bg="#2E4053", width=900, height=100)
    top_frame.place(x=0, y=0)
    Label(top_frame, text="🗣️ TEXT TO SPEECH", font=("Segoe UI", 22, "bold"), bg="#2E4053", fg="white").place(x=250, y=30)

    global text_area
    text_area = Text(root, font=("Segoe UI", 16), bg="white", relief=GROOVE, wrap=WORD)
    text_area.place(x=40, y=150, width=500, height=150)

    Label(root, text="Input Language:", font=("Segoe UI", 13, "bold"), bg="#34495E", fg="white").place(x=600, y=130)
    input_lang_combobox = Combobox(root, values=[name for name, code in LANGUAGES], font=("Segoe UI", 13), state='readonly', width=15)
    input_lang_combobox.place(x=600, y=160)
    input_lang_combobox.set('Hindi')

    Label(root, text="Speak In Language:", font=("Segoe UI", 13, "bold"), bg="#34495E", fg="white").place(x=600, y=200)
    output_lang_combobox = Combobox(root, values=[name for name, code in LANGUAGES], font=("Segoe UI", 13), state='readonly', width=15)
    output_lang_combobox.place(x=600, y=230)
    output_lang_combobox.set('English')

    Button(root, text="Speak", width=10, font=("Segoe UI", 14, "bold"), bg="#00B894", fg="white", relief=FLAT, command=speak_now).place(x=600, y=280)
    Button(root, text="Back", width=10, font=("Segoe UI", 14, "bold"), bg="#636E72", fg="white", relief=FLAT, command=show_main_menu).place(x=750, y=400)

def speech_to_text():
    def recognize_speech():
        recognizer = sr.Recognizer()
        input_lang_display = input_lang_combobox.get()
        output_lang_display = output_lang_combobox.get()
        input_lang_code = next((code for name, code in LANGUAGES if name == input_lang_display), None)
        output_lang_code = next((code for name, code in LANGUAGES if name == output_lang_display), None)
        with sr.Microphone() as source:
            try:
                text_area.delete(1.0, END)
                show_message("🎧 Listening...")
                audio = recognizer.listen(source, timeout=15)
                show_message("🔍 Recognizing...")
                text = recognizer.recognize_google(audio, language=input_lang_code)
                # Translate recognized text to output language
                if input_lang_code != output_lang_code:
                    translator = Translator(from_lang=input_lang_code, to_lang=output_lang_code)
                    translated_text = translator.translate(text)
                else:
                    translated_text = text
                text_area.insert(END, translated_text)
                show_message("✅ Done.")
            except sr.UnknownValueError:
                show_message("Could not understand audio.")
            except sr.RequestError as e:
                show_message(f"Speech recognition error: {e}")
            except Exception as e:
                show_message(f"Unexpected error: {e}")

    clear_window()
    top_frame = Frame(root, bg="#2E4053", width=900, height=100)
    top_frame.place(x=0, y=0)
    Label(top_frame, text="🎙️ SPEECH TO TEXT", font=("Segoe UI", 22, "bold"), bg="#2E4053", fg="white").place(x=250, y=30)

    global text_area
    text_area = Text(root, font=("Segoe UI", 14), bg="white", relief=GROOVE, wrap=WORD)
    text_area.place(x=40, y=150, width=500, height=120)

    Label(root, text="Speak In Language:", font=("Segoe UI", 13, "bold"), bg="#34495E", fg="white").place(x=600, y=130)
    input_lang_combobox = Combobox(root, values=[name for name, code in LANGUAGES], font=("Segoe UI", 13), state='readonly', width=15)
    input_lang_combobox.place(x=600, y=160)
    input_lang_combobox.set('Hindi')

    Label(root, text="Translate To:", font=("Segoe UI", 13, "bold"), bg="#34495E", fg="white").place(x=600, y=200)
    output_lang_combobox = Combobox(root, values=[name for name, code in LANGUAGES], font=("Segoe UI", 13), state='readonly', width=15)
    output_lang_combobox.place(x=600, y=230)
    output_lang_combobox.set('English')

    Button(root, text="Record", width=10, font=("Segoe UI", 14, "bold"), bg="#0984E3", fg="white", relief=FLAT, command=recognize_speech).place(x=600, y=280)
    Button(root, text="Back", width=10, font=("Segoe UI", 14, "bold"), bg="#636E72", fg="white", relief=FLAT, command=show_main_menu).place(x=750, y=400)

def speech_to_speech():
    def recognize_and_speak():
        recognizer = sr.Recognizer()
        input_lang_display = input_lang_combobox.get()
        output_lang_display = output_lang_combobox.get()
        input_lang_code = next((code for name, code in LANGUAGES if name == input_lang_display), None)
        output_lang_code = next((code for name, code in LANGUAGES if name == output_lang_display), None)
        with sr.Microphone() as source:
            try:
                show_message("🎧 Listening...")
                audio = recognizer.listen(source, timeout=15)
                show_message("🔍 Recognizing...")
                text = recognizer.recognize_google(audio, language=input_lang_code)
                # Translate recognized text to output language
                if input_lang_code != output_lang_code:
                    translator = Translator(from_lang=input_lang_code, to_lang=output_lang_code)
                    translated_text = translator.translate(text)
                else:
                    translated_text = text
                # Speak the translated text in output language
                tts = gTTS(translated_text, lang=output_lang_code, slow=False)
                tts.save("output.mp3")
                os.system("start output.mp3")
                show_message(f"Spoken: {translated_text}")
            except sr.UnknownValueError:
                show_message("Could not understand audio.")
            except sr.RequestError as e:
                show_message(f"Speech recognition error: {e}")
            except Exception as e:
                show_message(f"Unexpected error: {e}")

    clear_window()
    top_frame = Frame(root, bg="#2E4053", width=900, height=100)
    top_frame.place(x=0, y=0)
    Label(top_frame, text="🔊 SPEECH TO SPEECH", font=("Segoe UI", 22, "bold"), bg="#2E4053", fg="white").place(x=250, y=30)

    Label(root, text="Speak In Language:", font=("Segoe UI", 13, "bold"), bg="#34495E", fg="white").place(x=200, y=180)
    input_lang_combobox = Combobox(root, values=[name for name, code in LANGUAGES], font=("Segoe UI", 13), state='readonly', width=15)
    input_lang_combobox.place(x=200, y=210)
    input_lang_combobox.set('Hindi')

    Label(root, text="Speak Out Language:", font=("Segoe UI", 13, "bold"), bg="#34495E", fg="white").place(x=500, y=180)
    output_lang_combobox = Combobox(root, values=[name for name, code in LANGUAGES], font=("Segoe UI", 13), state='readonly', width=15)
    output_lang_combobox.place(x=500, y=210)
    output_lang_combobox.set('English')

    Button(root, text="Speak", width=10, font=("Segoe UI", 14, "bold"), bg="#fdcb6e", fg="#2d3436", relief=FLAT, command=recognize_and_speak).place(x=380, y=270)
    Button(root, text="Back", width=10, font=("Segoe UI", 14, "bold"), bg="#636E72", fg="white", relief=FLAT, command=show_main_menu).place(x=750, y=400)

def show_message(msg):
    if hasattr(show_message, 'msg_label') and show_message.msg_label:
        show_message.msg_label.destroy()
    show_message.msg_label = Label(root, text=msg, font=("Segoe UI", 12), bg="#2E4053", fg="#FFB347")
    show_message.msg_label.place(x=40, y=430)
    root.after(3000, show_message.msg_label.destroy)

# Main window setup
root = tk.Tk()
root.title("TEXT-SPEECH Translator")
root.geometry("900x500")
root.resizable(False, False)
root.configure(bg="#34495E")

# Combobox theme
style = Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="white", background="white", foreground="black")

show_main_menu()
root.mainloop()
