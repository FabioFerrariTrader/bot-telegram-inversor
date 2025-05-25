from telethon.sync import TelegramClient, events, Button
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do .env
load_dotenv()

# Variáveis de configuração seguras
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
grupo_origem = int(os.getenv("GRUPO_ORIGEM"))
grupo_destino = int(os.getenv("GRUPO_DESTINO"))

# Inicializa cliente Telegram
client = TelegramClient('sessao_inversor', api_id, api_hash)

# Estado do bot
modo_observador = True
contador_wins = 0
modo_disparo = False
ignorar_proxima = False

@client.on(events.NewMessage(chats=grupo_origem))
async def monitorar_mensagens(event):
    global modo_observador, contador_wins, modo_disparo, ignorar_proxima

    texto = event.raw_text.upper()
    print(f"Mensagem recebida: {texto}")

    if "EURJPY-OTC" in texto:
        ignorar_proxima = True
        print("Ignorando próxima mensagem devido a EURJPY-OTC")
        return
    if ignorar_proxima:
        ignorar_proxima = False
        print("Mensagem ignorada após EURJPY-OTC")
        return

    if modo_observador:
        if "WIN" in texto and "LOSS" not in texto:
            contador_wins += 1
            print(f"WIN detectado - contador: {contador_wins}")
            if contador_wins >= 3:
                modo_observador = False
                modo_disparo = True
                print("Entrando no modo disparo")
        elif "LOSS" in texto:
            contador_wins = 0
            print("LOSS detectado - contador zerado")

    elif modo_disparo:
        mensagem_modificada = texto

        if "ACIMA" in texto:
            mensagem_modificada = mensagem_modificada.replace("ACIMA", "PUT")
        if "ABAIXO" in texto:
            mensagem_modificada = mensagem_modificada.replace("ABAIXO", "CALL")
        if "WIN" in texto:
            mensagem_modificada = "LOSS? VAMOS RECUPERAR!"
        if "LOSS" in texto:
            mensagem_modificada = "WIN SEM GALE ✅✅✅"

        print(f"Enviando mensagem modificada: {mensagem_modificada}")
        await client.send_message(
            grupo_destino,
            mensagem_modificada,
            buttons=[Button.url("Acesse a Corretora!", "https://abrir.link/lJZsp")]
        )

        if "LOSS" in texto:
            modo_observador = True
            modo_disparo = False
            contador_wins = 0
            print("LOSS detectado - retornando ao modo observador")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está ativo!"

def iniciar_flask():
    app.run(host="0.0.0.0", port=8080)

def iniciar_bot():
    with client:
        print("Bot iniciado.")
        client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=iniciar_flask).start()
    iniciar_bot()
