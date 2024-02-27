import json

import requests
import telebot

TOKEN = '6949477339:AAFMfF-e0Nad2ph9AzxRDbWgXSC6emKkcPI'
bot = telebot.TeleBot(TOKEN)

def post_request(license_url, pssh):
    api_url = "https://keysdb.net/api"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Ktesttemp, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Content-Type": "application/json",
        "X-API-Key": 'b17b4bd17f2147e7bd7c88be5402af71517e2d46bddbedbcc29afa784da0d5c7',
    }
    payload = {
        "license_url": license_url,
        "pssh": pssh,
    }
    r = requests.post(api_url, headers=headers, json=payload)
    r_json = r.json()
    keys = r_json.get('keys', [{}])[0]
    return f"key: {keys.get('key')}\nkid: {r_json.get('kid')}\nlicense_url: {keys.get('license_url')}"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya adalah bot Minta Key")

@bot.message_handler(commands=['key'])
def handle_post(message):
    # Split the message text into parts
    parts = message.text.split(maxsplit=2)
    if len(parts) != 3:
        bot.reply_to(message, "Format pesan salah. Harusnya: /post <url> <pssh>")
        return

    _, license_url, pssh = parts
    response = post_request(license_url, pssh)
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
