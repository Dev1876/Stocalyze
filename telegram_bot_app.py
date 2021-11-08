import os
import ast
import logging
from sqlalchemy.engine.interfaces import Dialect
from telegram.update import Update
from strategysignal import StrategySignal
import locale
from telegram.ext.messagehandler import MessageHandler
from models import *
from telegram import ParseMode
from database import SessionLocal
from ticker import Ticker as T
from configparser import SafeConfigParser
from typing import Dict

from telegram import(
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import(Updater,
CommandHandler,
CallbackContext,
ConversationHandler,
Filters)

#export TELEGRAM_BOT_TOKEN= '742984207'
#https://levelup.gitconnected.com/how-to-code-a-telegram-bot-to-get-stock-price-updates-in-pure-python-c35d3c44b04c

#set locale & enable logging
locale.setlocale(locale.LC_ALL,'')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
#TOKEN = '742984207:AAEPz6Wb37zMkB9g28wHz1z-cMNS5MiOnaQ'
PORT = os.getenv('PORT', default=8443)
#JuniorMarket = JuniorMarket()
#Jstock_list = JuniorMarket.GetJuniorMarketListed()

logger = logging.getLogger(__name__)
#PORT = int(os.environ.get())
VERB = ["BUY","SELL"]
COLOUR = ["🔴", "🟢"]

DEFAULT_PORT = {
    "JMMBGL": 200,
    "SVL": 50
}



UPDATED =0
CHOICE_MAP = {
    "remove from stock portfolio": "-portfolio",
    "add to stock portfolio": "+portfolio",
    "add to watchlist": "+watchlist",
    "remove from watchlist": "-watchlist"
}
reply_keyboard = [
    ["Add to stock portfolio", "Add to watchlist"],
    ["Remove from stock portfolio", "Remove from watchlist"],
    ["Portfolio updates", "Watchlist updates"],
    ["Subscribe/Unsubscribe to daily updates", "Done"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

user = User()
db = SessionLocal()



def get_ticker_signal(update: Update, context: CallbackContext,stocks: str =None,type:str="command") -> None:
    message = f"📈 Here are your current market updates:\n" \
              f"(Note: there may be a one Day delay)\n"
    if type =="command":
        if not stocks:
            stocks = update.message.text.split('/get_ticker_signal')[1].strip()
            stocks = stocks.split()
    elif type =="conversation":
        stocks = ast.literal_eval(stocks)

    for _, stock in enumerate(stocks):
        
        print(T)
        psar_sign = StrategySignal(stock).GetSuperTrend()
        trad_sig = ''
        if psar_sign:
            trad_sig = "BUY"
        else:
            trad_sig = "SELL"
        message += f"{stock.upper()} latest Trading Signal is {trad_sig}{COLOUR[psar_sign]}\n"
    
    

    update.message.reply_text(message)


def update_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user["id"]
    user =  User.get_user(db, user_id)
    context.user_data.update(user())

    text = update.message.text.lower()
    
    #user_input = text in CHOICE_MAP.keys()
    
    #print(user_input)
    #context.user_data['choice'] = CHOICE_MAP[text]
    #if user_input:
    context.user_data['choice'] = CHOICE_MAP[text]
    if context.user_data.get(text):
        reply_text = (
                f'Your {text}, I already know the following about that: '
                f'{context.user_data[text]}'
                )
    else:
        reply_text = (
                f'You want to {text}? Please add or remove stocks '
                f'by listing them by their ticker, separated by a space. '
                f'Example: \n\n GK JSE DTL'
                )
    #else:
       
      
    update.message.reply_text(reply_text)

    return UPDATED



def get_default_port(update: Update, context: CallbackContext,
                     portfolio: Dict = None) -> None:
    # Set portfolio
    port = T(portfolio) if portfolio else T(DEFAULT_PORT)

    # Stock level updates
    get_ticker_signal(update, context, DEFAULT_PORT)

    # Portfolio level updates
    #port_change, pctg_port_change, new_port_val = port.get_portfolio_change()
    update.message.reply_text(
        f"Your portfolio of {len(port)} stocks " #Dict
        #f"by {port_change:.2f} ({pctg_port_change:.2f}%).\n\n Your "
        #f"portfolio value is now {int(new_port_val):n}."
    )

def provide_updates(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user["id"]
    user = User.get_user(db, user_id)
    context.user_data.update(user())

    text = update.message.text.lower()
    context.user_data['choice'] = text

    # Catch if user tries to get updates before updating portfolio/watchlist
    if text.split()[0] in context.user_data.keys():
        stocks = context.user_data[text.split()[0]]

        get_ticker_signal(update=update, context=context, stocks=stocks,
                      type="conversation")
    else:
        update.message.reply_text(
            f"No stocks found in your {text.split()[0]}! "
            f"Please select the update options before getting updates."
        )
    update.message.reply_text(
        "What would you like to do next?",
        reply_markup=markup
    )



def received_information(update: Update, context: CallbackContext) -> None:
    stocks = (update.message.text).lower().split()
    category = context.user_data['choice']
    choice, category = category[0], category[1:]

    # Get the user from DB
    user_id = update.message.from_user["id"]
    user = User.get_user(db, user_id)

    # Check if add or remove to portfolio or watchlist
    if category == "portfolio":
        to_update = ast.literal_eval(getattr(user, category))
    elif category == "watchlist":
        to_update = ast.literal_eval(getattr(user, category))

    for stock in stocks:
        try:
            if choice == "-":
                to_update.remove(stock)
            else:
                to_update.append(stock)
        
            # Update the database
            setattr(user, category, str(to_update))
            User.update_userdb(db, user)

            # Update the context data for facts_to_str
            context.user_data[category] = str(to_update)
            del context.user_data['choice']

        except:
            update.message.reply_text(
                f"Failed to update your {category} with {stock}!"
                f"\n\nPlease check if {stock} exists in your {category}."
            )

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:\n"
        f"{facts_to_str(context.user_data)}\n"
        "You can tell me more, or change your opinion on "
        "something.",
        reply_markup=markup,
    )

    return ConversationHandler.END


def start(update: Update, context: CallbackContext) -> None:
    reply_text = "Hi! I am your personal Stock Bot, sbot 🤖.\n"

    user_id = update.message.from_user["id"]
    user =  User.get_user(db, user_id)

    if not (user.portfolio or user.watchlist):
        reply_text += (
            "\nYou have not informed me of your stock portfolio and/or "
            f"watchlist."
        )
    else:
        context.user_data.update(user())
        reply_text += (
            f"{facts_to_str(context.user_data)}"
        )

    reply_text += "\n\nHow may I be of service today?"
    update.message.reply_text(reply_text, reply_markup=markup)



def facts_to_str(user_data):
    facts = "\n📝 Portfolio: \n\n"
    
    port = ast.literal_eval(user_data["portfolio"])
    facts += "\n".join(p.upper() for p in port)

    facts += "\n\n👀 Watchlist: \n\n"
    watch = ast.literal_eval(user_data["watchlist"])
    facts += "\n".join(p.upper() for p in watch)

    subscribed = "YES" if user_data["is_subscribed"] else "NO"
    facts += f"\n\nSubscription to daily updates: {subscribed}\n"

    return facts

def done(update: Update, context: CallbackContext) -> None:
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text(
        f"Thank you for using Stock Bot Slave 😊 !\n"
        f"To get a summary of what you've told me, please select /start.\n"
        f"To update or get updates on your portfolio/watchlist, please "
        f"use the markup keyboard."
    )
    return ConversationHandler.END


def toggle_subscription(update: Update, context: CallbackContext) -> None:
    # Get user & subscription status
    user_id = update.message.from_user["id"]
    user = User.get_user(db, user_id)
    filler = "" if user.is_subscribed else " not"
    toggle = "off" if user.is_subscribed else "on"
    db_update = False if user.is_subscribed else True

    # Update is_subscribed status in DB
    try:
        setattr(user, "is_subscribed", db_update)
        User.update_userdb(db, user)

        update.message.reply_text(
            f"📲 *What are daily updates?*\n"
            f"Daily updates are push notifications informing you of end of "
            f"day price changes to your portfolio/watchlist stocks. They are "
            f"sent out daily at 8 PM UTC and 9 AM UTC. These times correspond"
            f" to US and Singapore market closing times.\n\n"
            #f"Looks like you are{filler} subscribed to daily "
            f"portfolio/watchlist updates. Toggling subscription status "
            #f"{toggle}.",
            #parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(e)
        update.message.reply_text("Failed to update your subscription status.")


def main() -> None:
    updater = Updater(TOKEN,use_context=True)

    #get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    #Add conversation handler to ask for user's stock portfolio/watchlist
    conv_handler = ConversationHandler(
        entry_points=[
           MessageHandler(
               Filters.regex(
                '^(Add to stock portfolio|Add to watchlist|Remove from watchlist|Remove from stock portfolio)$'
                ), update_user
            )
        ],
        states={
            UPDATED:[
                MessageHandler(
                    Filters.text & ~(Filters.command|Filters.regex('^Done$')),
                    received_information
                    #update_user
                )
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'),done)],
        name="updates",
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)
    
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                '^(Portfolio updates|Watchlist updates)$'
                ),provide_updates
        )
    )

    dispatcher.add_handler(MessageHandler(
        Filters.regex(
            '^Subscribe/Unsubscribe to daily updates$'
        ),toggle_subscription
    ))

    dispatcher.add_handler(MessageHandler(Filters.regex('^Done'),done))
    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler("get_ticker_signal",get_ticker_signal))
    dispatcher.add_handler(CommandHandler("default",get_default_port))



#Start the Bot
# 'start_polling' for local dev; webhook for production
# updater.start_polling()

    #updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url='https://stockegy-bot.herokuapp.com/'+TOKEN)  
    #Start teh Bot
    updater.start_polling()

     # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.

    updater.idle()

if __name__ == "__main__":
    main()
