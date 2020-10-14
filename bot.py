import requests
import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = "1268034504:AAH0rzkFXpCs0XESJZBNj76sNZ0vRDOOx3g"
def start(update, context):
    update.message.reply_text('Hi!'+"  "+str(update.message.from_user.username))
    context.bot.send_message(chat_id=update.effective_chat.id , text="use /help to know more")
    
def randdog(update, context):
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    context.bot.sendPhoto(chat_id=update.effective_chat.id,photo=url)

def randcat(update, context):
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    context.bot.sendPhoto(chat_id=update.effective_chat.id,photo=contents[0]['url'])


def randomfact(update,context):
    url = "https://numbersapi.p.rapidapi.com/random/date"
    querystring = {"max": "20", "fragment": "true", "min": "10", "json": "true"}
    headers = {
        'x-rapidapi-host': "numbersapi.p.rapidapi.com",
        'x-rapidapi-key': "b0d868a5e5msh6e7d002462710bdp19baacjsn88068357c863"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    context.bot.send_message(chat_id=update.effective_chat.id,text=response["text"])

def adviceplz(update, context):
    contents = requests.get('https://api.adviceslip.com/advice').json()
    url = contents['slip']['advice']
    context.bot.send_message(chat_id=update.effective_chat.id,text=url)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(' my commands are')
    update.message.reply_text('/start')
    update.message.reply_text('/randomfact  to get random facts')
    update.message.reply_text('/randdog  to get random dog pictures')
    update.message.reply_text('/adviceplz  to get advice from me and trust me i am a good advisor')
    update.message.reply_text('And trust me i am a good advisor')
    update.message.reply_text('for any improvements or suggestions contact @inokiyoshida ')
def message(update, context):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    from pprint import pprint
    querystring = {"term": update.message.text}

    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "b0d868a5e5msh6e7d002462710bdp19baacjsn88068357c863"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    k=random.randint(0,9)
    try:
        context.bot.send_message(chat_id=update.effective_chat.id,text=str(response['list'][k].get("definition")))
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry ! i dont know about that but i will answer u next time")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('randomfact', randomfact))
    dp.add_handler(CommandHandler('adviceplz',adviceplz))

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text&(~Filters.command), message))
    dp.add_handler(CommandHandler('randdog', randdog ))
    dp.add_handler(CommandHandler('randcat', randcat))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://shrouded-hollows-46047.herokuapp.com/' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
