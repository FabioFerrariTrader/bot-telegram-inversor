from telethon import TelegramClient, events
from telegram import Bot

api_id = 28664878
api_hash = "6bed082ff2a1fb82661440e4eccf79df"
bot_token = "7504359239:AAEmf8i_htNIyGIPZ7OrwDUEqfcEecGyKRI"

canal_origem = -1002392524513
canal_destino = -1002655261655

client = TelegramClient('sinais', api_id, api_hash)
import os
bot_token = os.getenv("BOT_TOKEN")

def inverter_sinal(mensagem):
    return mensagem.replace('ABAIXO', 'CALL').replace('ACIMA', 'PUT')

@client.on(events.NewMessage(chats=canal_origem))
async def handler(event):
    texto = event.message.message
    texto_invertido = inverter_sinal(texto)
    await bot.send_message(chat_id=canal_destino, text=texto_invertido)

client.start()
client.run_until_disconnected()

