from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# Wstaw tutaj token swojego bota z BotFather
TELEGRAM_TOKEN = 'YOUR_BOT_API_TOKEN'

# Adres API Twojej aplikacji FastAPI
API_URL = 'https://twoja-aplikacja.onrender.com/separate'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Witaj! Prześlij mi plik audio, a ja go przetworzę.")

def handle_audio(update: Update, context: CallbackContext) -> None:
    # Pobieramy plik audio
    audio_file = update.message.audio.get_file()
    file_path = f"downloads/{audio_file.file_id}.ogg"
    
    # Pobieramy plik na lokalny dysk
    audio_file.download(file_path)
    
    # Wysyłamy plik do naszego API FastAPI
    with open(file_path, 'rb') as audio:
        files = {'file': audio}
        response = requests.post(API_URL, files=files)
    
    # Jeśli odpowiedź z API jest poprawna, wysyłamy plik do użytkownika
    if response.status_code == 200:
        with open('output_audio/vocals.wav', 'rb') as f:
            update.message.reply_audio(audio=f)
    else:
        update.message.reply_text("Wystąpił błąd podczas przetwarzania pliku.")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))  # Przechwytujemy pliki audio
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
