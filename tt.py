import requests
import telebot

TOKEN = '5816289875:AAGB_rDNTISvxyGLZ2NunN9d2l3No4RzYGo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'tt'])
def send_welcome(message):
    bot.reply_to(message, "Selamat datang saya adalah bot untuk mengunduh video dari tiktok*\n\n*Caranya :* _Tinggal kirimkan saja link tiktok ke bot ini dan nanti anda akan di kirimkan video sesuai link_")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.startswith('https://vt.tiktok.com/'):
        url = f"https://api.lolhuman.xyz/api/tiktok?apikey=beb6de5dced2bc7aca60e726&url={message.text}"
        response = requests.get(url)
        result = response.json()
        video_url = result['result']['link']
        video_data = requests.get(video_url).content
        with open('video.mp4', 'wb') as f:
            f.write(video_data)
        video = open('video.mp4', 'rb')
        bot.send_video(message.chat.id, video)
    else:
        api_url = f"https://api.lolhuman.xyz/api/tiktokwm?apikey=beb6de5dced2bc7aca60e726&url={message.text}"
        bot.reply_to(message, api_url)

bot.polling()
