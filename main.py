import telebot
import requests
from config import BOT_TOKEN, API_URL, CHAT_ID
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
WEBHOOK_URL = "https://ipl-betting-bot.onrender.com/webhook"

app = Flask(__name__)

def fetch_match_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()

def analyze_session(data):
    score = data['score']
    overs = data['overs']
    run_rate = score / overs

    if run_rate > 10:
        return "YES, likely to cross target"
    else:
        return "NO, unlikely to cross target"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "Webhook received", 200

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I'll provide session tips. Use /session to get updates.")

@bot.message_handler(commands=['session'])
def send_session_update(message):
    match_data = fetch_match_data()
    if match_data:
        prediction = analyze_session(match_data)
        bot.send_message(CHAT_ID, f"Session Prediction: {prediction}")
    else:
        bot.send_message(CHAT_ID, "Error fetching match data. Try again later.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
