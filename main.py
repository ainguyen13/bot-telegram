import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/vietai/wkspaces/master-python/credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1JGvQqoYx0ThNqsFhjSHxTAQg4NO9NFYbJL7cpDzcN_Q').sheet1

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    sheet_url = "https://docs.google.com/spreadsheets/d/1JGvQqoYx0ThNqsFhjSHxTAQg4NO9NFYbJL7cpDzcN_Q/edit"
    update.message.reply_text(f'Welcome to the Expense Tracker Bot! Send your expenses in the format: Category Description Amount\nYou can view your expenses here: {sheet_url}')

# Define the message handler for recording expenses
def record_expense(update: Update, context: CallbackContext) -> None:
    try:
        if update.message is None:
            logger.error('Received update with no message')
            return

        text = update.message.text
        parts = text.split(' ')
        if len(parts) < 3:
            update.message.reply_text('Error recording expense. Please use the format: Category Description Amount')
            return

        category = parts[0]
        description = ' '.join(parts[1:-1])
        amount = parts[-1]

        # Append the expense to the Google Sheet
        sheet.append_row([category, description, amount])

        update.message.reply_text(f'Recorded: {category} {description} {amount}')
    except Exception as e:
        if update.message:
            update.message.reply_text('Error recording expense. Please use the format: Category Description Amount')
        logger.error(f'Error recording expense: {e}')

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your bot's API token
    application = Application.builder().token('7239809175:AAGSfH9NgpoDLDCvYMngvBz2CASVQtGqVZs').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, record_expense))

    # Run the application using the default event loop
    application.run_polling()

if __name__ == '__main__':
    main()