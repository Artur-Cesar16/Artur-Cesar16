import requests
import info
from env import token

def enviarMensagem(id_chat, mensagem):
    dados = {'chat_id':id_chat, 'text': mensagem}
    post = requests.post(f'https://api.telegram.org/bot{token}/sendMessage',data=dados)



def telegramInteraction():
    offset = 1
    
    while True:
        url_base = ''

        #Se for o primeiro loop, ele não precisa ter offset
        if offset == 1:
            url_base = f'https://api.telegram.org/bot{token}/getUpdates?timeout=2'
        else:
            url_base = f'https://api.telegram.org/bot{token}/getUpdates?timeout=2&offset={offset+1}'
        
        retorno = requests.get(url_base)
        data = retorno.json()
    
        for update in data['result']:

            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                mensagem = update['message']['text']
                nome_contato = update['message']['from']['first_name']

                if mensagem == '/info':
                    enviarMensagem(chat_id, info.info_redes())
                elif mensagem == '/ping':
                    enviarMensagem(chat_id, info.tempo_medio_de_ping())
                elif mensagem == '/active':
                    enviarMensagem(chat_id, info.resposta_ip())
                elif mensagem == '/dns':
                    enviarMensagem(chat_id, info.dns())
                elif mensagem == '/download':
                    enviarMensagem(chat_id, 'Envie a imagem por aqui ou digite o link da imagem iniciantdo com >http< ou >https<.')
                elif 'http' in mensagem or 'https' in mensagem:
                    enviarMensagem(chat_id, info.download_imagem(mensagem))
                else:
                    enviarMensagem(chat_id, f'Olá, {nome_contato}. Escolha uma das opções ao lado do seu input de mensagem para saber mais.')

                print(f'Chat ID: {chat_id}\nMensagem: {mensagem}\nPor: {update["message"]["from"]["first_name"]}')

                offset =  update['update_id'] #Para que ela não retorno de novo nos updates
            elif 'message' in update and 'photo' in update['message']:
                chat_id = update['message']['chat']['id']
                file_id = update['message']['photo'][1]['file_id']
               
                enviarMensagem(chat_id, info.download_imagem_do_telegram(file_id))
                offset =  update['update_id'] #Para que ela não retorno de novo nos updates
