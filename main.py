from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Reemplaza con el Token que te dio BotFather
TOKEN = '8671399670:AAF3J-weyP6Dq8KrbPOH1jeSSeByd9rWsAU'

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hola {update.effective_user.first_name}, soy tu bot de automatización. ¿En qué puedo ayudarte?"
    )

# Función para el comando /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Puedes usar /start para saludar o /info para saber más.")

if __name__ == '__main__':
    # Construimos la aplicación del bot
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Registramos los comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    
    print("Bot en marcha... Presiona Ctrl+C para detenerlo.")
    app.run_polling()