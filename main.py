from multiprocessing import context

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
    await update.message.reply_text("A continuación te mostraré la lista de los comandos disponibles:\n\n/start - Inicia la conversación con el bot\n"
    "/ayuda - Muestra esta ayuda\n/recordatorio - Puedes crear un recordatorio")

async def enviar_alarma(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    # Usamos job.chat_id que guardamos al programarlo
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text=f"⏰ ¡Es hora de tu recordatorio!: {job.data}"
    )
# funcion para programar un recordatorio
from datetime import datetime, time, timedelta
async def programar_recordatorio(update, context):
    chat_id = update.effective_message.chat_id
    ahora = datetime.now()
    
    # 1. Validar que el usuario escribió algo después del comando
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Uso: /recordar HH:MM mensaje\nEjemplo: /recordar 18:50 pastilla")
        return

    try:
        tiempo_input = context.args[0].strip()
        mensaje = " ".join(context.args[1:])

        if ":" in tiempo_input:
            hora_partes = tiempo_input.split(":")
            h, m = int(hora_partes[0]), int(hora_partes[1])
            
            # Crear objetivo con la hora de hoy
            objetivo = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
            
            # Si la hora ya pasó, sumar un día
            if objetivo < ahora:
                objetivo += timedelta(days=1)
            
            segundos = (objetivo - ahora).total_seconds()
            
            # IMPORTANTE: Asegúrate que la función se llame 'enviar_alarma'
            context.job_queue.run_once(enviar_alarma, segundos, data=mensaje, chat_id=chat_id)
            
            await update.message.reply_text(f"✅ ¡Listo! Te avisaré a las {tiempo_input}.")
        else:
            await update.message.reply_text("❌ Formato de hora incorrecto. Usa HH:MM (ejemplo 18:30)")

    except Exception as e:
        print(f"Error interno: {e}") # Mira esto en tu terminal de VS Code
        await update.message.reply_text("❌ Hubo un error al procesar la hora. Intenta de nuevo.")
    


if __name__ == '__main__':
    # Construimos la aplicación del bot
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Registramos los comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("recordatorio", programar_recordatorio))
    print("Bot en marcha... Presiona Ctrl+C para detenerlo.")
    app.run_polling()