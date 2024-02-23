import os

import telebot

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
bot = telebot.TeleBot('6719405878:AAFdAfGbpoOkaw1KTvcn7Mr-IJp2ZxACzsQ')

user_data = {}

@bot.message_handler(commands=['html'])
def generate_html(message):
    bot.send_message(message.chat.id, "Masukkan URL Video:")
    bot.register_next_step_handler(message, process_video_url_step)

def process_video_url_step(message):
    try:
        user_data[message.chat.id] = {"video_file_url": message.text.strip()}
        bot.send_message(message.chat.id, "Masukkan judul Video:")
        bot.register_next_step_handler(message, process_title_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

def process_title_step(message):
    try:
        user_data[message.chat.id]["title"] = message.text.strip()
        bot.send_message(message.chat.id, "Masukkan URL Thumbnail:")
        bot.register_next_step_handler(message, process_image_step)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

def process_image_step(message):
    try:
        user_data[message.chat.id]["image"] = message.text.strip()

        html_code = f"""
        <!DOCTYPE html>
        <head>
            <title>LIVE EVENT STREAMING</title>
            <!-- Other meta tags and head content -->

            <script src="https://ssl.p.jwpcdn.com/player/v/8.25.1/jwplayer.js"></script>
            <script> jwplayer.key = 'Mh/98M9sROX0uXhFlJwXZYeCxbJD5E1+e2goFcRZ07cI/FTu'; </script>

            <style type="text/css">
                html, body {{
                    width:100%;
                    height: 100%;
                    font-family: Poppins;
                    display:block;
                    position: absolute;
                    padding: 0px;
                    margin: 0px;
                    background: #000;
                    overflow: hidden;
                }}
                .player {{
                    width:100%;
                    height: 100%;
                    display:inline-block;
                    -webkit-user-select:none;
                    -moz-user-select:none;
                    -ms-user-select:none;
                    user-select:none;
                }}
            </style>
        </head>
        <body>
            <div id="player"></div>
            <script>
                var playerInstance = jwplayer("player");

                playerInstance.setup({{
                    playlist: [{{
                        "title": "{user_data[message.chat.id]['title']}",
                        "image": "{user_data[message.chat.id]['image']}",
                        sources: [{{file: '{user_data[message.chat.id]["video_file_url"]}'}}],
                        tracks: [{{file: '', "kind": 'captions', "label": 'Indonesia', "default": true}}],
                        }}],
                    width: "100%",
                    height: "100%",
                    "stretching": "exactfit",
                    autostart: false,
                    "mute": false,
                    "volume": 25,
                    logo: {{
                        file: 'https://i.postimg.cc/7hBXqptn/tipion.png',
                        link: '',
                        hide: 'false',
                        margin: '35',
                        over: '15',
                        out: '79.5',
                        position: 'bottom-right'
                    }},
                    skin: {{
                        controlbar: {{
                            background: 'rgba(0,0,0,0)',
                            icons: '#FFFFFF',
                            iconsActive: '#FF0000',
                            text: '#FFFFFF',
                        }},
                    }},
                    pipIcon:{{}},
                    cast:{{}}
                }});
            </script>
        </body>
        </html>
        """

        html_filename = f"generated_html_{message.chat.id}.html"
        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html_code)

        with open(html_filename, 'rb') as file:
            bot.send_document(message.chat.id, file)

        os.remove(html_filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

# Start the bot
bot.polling()