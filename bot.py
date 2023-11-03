import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, PicklePersistence
from config import BOT_API
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import telegram

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

CHOOSING, IMG = range(2)

keyboard = [['🖼 Remove Background'], ['🧑‍💻 Contact Us', '💰 Support']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        'Welcome to The Background Remover Bot',
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )

    return CHOOSING

async def img_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['🔙']]

    await update.message.reply_text(
        'Please send me your img so I can remove the background',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )

    return IMG

async def handle_img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    