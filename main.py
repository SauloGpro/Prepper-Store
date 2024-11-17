import telebot
from handlers import commands, callbacks

# Token del bot
TOKEN = '7929103907:AAEyNM9tXI10LKaVlYpEWsGFXakgJcj2CIA'
bot = telebot.TeleBot(TOKEN)

# Registrar comandos
commands.register_commands(bot)
callbacks.register_callbacks(bot)

# Mantener el bot funcionando
bot.polling()



