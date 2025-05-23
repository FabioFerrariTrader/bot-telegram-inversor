from telethon.sync import TelegramClient, events

# Substitua com seus dados
api_id = 28664878
api_hash = "6bed082ff2a1fb82661440e4eccf79df"

# IDs dos grupos
grupo_origem = -1002392524513
grupo_destino = -1002655261655

# Inicializa o cliente
with TelegramClient('sessao_bot', api_id, api_hash) as client:

    @client.on(events.NewMessage(chats=grupo_origem))
    async def handler(event):
        texto = event.raw_text

        # Substituição dos sinais
        texto_modificado = texto.replace("ABAIXO", "CALL").replace("ACIMA", "PUT")

        # Envia para o grupo de destino
        await client.send_message(grupo_destino, texto_modificado)

    print("BOT ATIVO - Monitorando mensagens... (Pressione Ctrl+C para parar)")
    client.run_until_disconnected()
