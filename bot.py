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
    img = update.message.photo[-1].file_id
    file = await context.bot.get_file(img)
    await file.download_to_drive(f'Data/{img}.jpg')
    await update.message.reply_photo(f'Data/{img}.jpg')
    
    return IMG

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Contact Us @ahmadrishi',
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''💳 You can support this bot using any of the following methods: 
                                    \n\n\nUSDT TRC20:\n`TGyvamGVzimHMvhJ8sdd3NSJjbikrqHy7V`\n\nUSDT BEP20:\n`0x1fbfe66d0c24e21f6fb93799616c92d103a50e44`''', 
                                    parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
    return CHOOSING

def main():
    pres = PicklePersistence('Data/bot')
    application = ApplicationBuilder().token(BOT_API).persistence(persistence=pres).build()
    conversation_handler = ConversationHandler(
        name='bgremover',
        entry_points=[CommandHandler('start', start)],
        persistent=True,
        allow_reentry=True,
        states={
            CHOOSING:[
                MessageHandler(filters.Regex("^🖼 Remove Background$"), img_entry),
                MessageHandler(filters.Regex("^🧑‍💻 Contact Us$"), contact),
                MessageHandler(filters.Regex("^💰 Support$"), support)
            ],
            IMG:[
                MessageHandler(filters.Regex("^🔙$"), start),
                MessageHandler(filters.PHOTO, handle_img)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), print('done'))],
    )

    application.add_handler(conversation_handler)
    application.run_polling()

main()