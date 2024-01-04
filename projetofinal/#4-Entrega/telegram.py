import requests, time

token = '6871814803:AAEK-gg1Cbx13B-MWsVErZWkh6osZh23Hc0'

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
            chat_id = update['message']['chat']['id']
            mensagem = update['message']['text']

            if mensagem == '/info':
                enviarMensagem(chat_id, 'Informações básicas sobre a rede (ip, máscara, gateway).')
            elif mensagem == '/ping':
                enviarMensagem(chat_id, 'Tempo médio de ping (quatro pacotes) entre a máquina do bot e seu gateway.')
            elif mensagem == '/active':
                enviarMensagem(chat_id, 'Informa se o ip está respondendo.')
            elif mensagem == '/dns':
                enviarMensagem(chat_id, 'Informa o servidor de DNS da máquina do bot.')
            elif mensagem == '/download':
                enviarMensagem(chat_id, 'Download de uma imagem da internet no servidor.')
            else:
                enviarMensagem(chat_id, f'Olá, {update["message"]["from"]["first_name"]}. Escolha uma das opções ao lado do seu input de mensagem para saber mais.')

            print(f'Chat ID: {chat_id}\nMensagem: {mensagem}\nPor: {update["message"]["from"]["first_name"]}')

            offset =  update['update_id'] #Para que ela não retorno de novo nos updates
            print(update)

