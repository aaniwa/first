import threading
import http.server
import socketserver
import os

# 🟢 Start your Telegram bot like before
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
import logging
import random

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram handlers
def start(update, context):
    update.message.reply_text("Welcome! to simple telegram bot", parse_mode=ParseMode.HTML)
    coin(update, context)

def coin(update, context):
    msg = "⚫️ face " if random.randint(1, 2) == 1 else "⚪️ cross"
    update.message.reply_text(msg)

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def run_bot():
    TOKEN = os.getenv("BOT_TOKEN") or "your-token-here"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('coin', coin))
    dp.add_error_handler(error_callback)
    updater.start_polling()
    updater.idle()

# 🟢 Dummy web server to keep Render happy
def run_web_server():
    PORT = int(os.environ.get("PORT", 10000))  # Render will inject PORT
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving dummy HTTP on port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    # Run both bot and server in parallel threads
    threading.Thread(target=run_bot).start()
    run_web_server()
