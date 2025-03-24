import telebot
import requests
from config import BOT_TOKEN, API_URL, CHAT_ID

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_match_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return None

def analyze_session(data):
    score = data['score']
    overs = data['overs']
    run_rate = score / overs

    # Simple prediction logic (can be improved with more data)
    if run_rate > 10:
        return "YES, likely to cross target"
    else:
        return "NO, unlikely to cross target"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I’ll provide session tips. Use /session to get updates.")

@bot.message_handler(commands=['session'])
def send_session_update(message):
    match_data = fetch_match_data()
    if match_data:
        prediction = analyze_session(match_data)
        bot.send_message(CHAT_ID, f"Session Prediction: {prediction}")
    else:
        bot.send_message(CHAT_ID, "Error fetching match data. Try again later.")

bot.polling()
