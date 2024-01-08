def obter_informacoes_rede():
    sistema_operacional = platform.system()

    if sistema_operacional == 'Windows':
        comando = 'ipconfig'
    elif sistema_operacional == 'Linux':
        comando = 'ifconfig'
    else:
        print("Sistema operacional não suportado.")
        return None

    try:
        resultado = subprocess.run([comando], capture_output=True, text=True, shell=True)

        if resultado.returncode != 0:
            print(f"Erro ao executar o comando {comando}")
            return None

        saida = resultado.stdout

        informacoes = {
            'Endereço IP': None,
            'Máscara de Sub-rede': None,
            'Gateway Padrão': None
        }

        for index, linha in enumerate(saida.splitlines(), start=0):
            if 'Endereço IPv4' in linha or 'IPv4 Address' in linha or 'inet' in linha or 'IPv4' in linha:
                informacoes['Endereço IP'] = linha.split(':')[-1].strip().split('%')[0].strip()
            elif 'Máscara de Sub-rede' in linha or 'Subnet Mask' in linha or 'mask' in linha or 'Sub-rede' in linha:
                informacoes['Máscara de Sub-rede'] = linha.split(':')[-1].strip()
            elif 'Gateway Padrão' in linha or 'Default Gateway' in linha or 'gateway' in linha or 'Gateway' in linha:
                if sistema_operacional == 'Windows':
                     informacoes['Gateway Padrão'] = saida.splitlines()[index+1].strip()
                else:
                    informacoes['Gateway Padrão'] = linha.split(':')[-1].strip().split('%')[1].strip()

        return informacoes
    except Exception as e:
        print(f"Erro ao obter informações de rede: {e}")
        return None
    
def info_redes():
    """
        Informações básicas sobre a rede (ip, máscara, gateway).
    """
    informacoes = obter_informacoes_rede()
 # Verifica se as informações necessárias foram obtidas
    if informacoes['Endereço IP'] and informacoes['Máscara de Sub-rede'] and informacoes['Gateway Padrão']:
        endereco_ip = ipaddress.IPv4Address(informacoes['Endereço IP'])
        mascara_rede = ipaddress.IPv4Address(informacoes['Máscara de Sub-rede'])
        gateway = ipaddress.IPv4Address(informacoes['Gateway Padrão'])

        return f"Endereço IP: {endereco_ip}\nMáscara de Rede: {mascara_rede}\nGateway: {gateway}"
    else:
        print("Não foi possível encontrar todas as informações necessárias na saída.")
        return None


def tempo_medio_de_ping():
    """
        Tempo médio de ping (quatro pacotes) entre a máquina do bot e seu gateway.
    """
    informacoes = obter_informacoes_rede()
    comando = f'ping {informacoes["Gateway Padrão"]}'
    try:
        resultado = os.popen(comando).read()

        saida = resultado
        tempo_medio = -1

        for index, linha in enumerate(saida.splitlines(), start=0):
            if 'ms' in linha:
                tempo_medio = linha.split(',')[-1].strip()
               

        tempo_medio = tempo_medio.split('=')[1]
        return f"Tempo médio de ping: {tempo_medio} "


    except Exception as e:
        print(f"Erro ao obter informações de rede: {e}")
        return None


def resposta_ip():
    """
        Informa se o ip está respondendo.
    """

    informacoes = obter_informacoes_rede()
    comando = f'ping {informacoes["Endereço IP"]}'
    try:
        resultado = os.popen(comando).read()

        saida = resultado
        resposta = "Sem resposta do IP."

        for index, linha in enumerate(saida.splitlines(), start=0):
            if 'Perdidos' in linha:
                resposta = linha.split(',')[-1].strip()
               
        if 'Perdidos = 0' in resposta:
            resposta = 'IP respondendo.'
    
        return resposta

    except Exception as e:
        print(f"Erro ao obter informações de rede: {e}")
        return None
    
def dns():
    """
        Informa o servidor de DNS da máquina do bot
    """

    comando = 'ipconfig/all'
    try:
        resultado = os.popen(comando).read()

        saida = resultado
        resposta = "Não encontrado"

        for index, linha in enumerate(saida.splitlines(), start=0):
            if 'Servidores DNS' in linha:
                resposta = saida.splitlines()[index+2].strip()

        return f'DNS: {resposta}'

    except Exception as e:
        print(f"Erro ao obter informações de rede: {e}")
        return None
 

def download_imagem(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"./imagens/{url.split('/')[-1]}", 'wb') as f:
            f.write(response.content)
            return 'Download feito!'
    else:
        return 'Erro ao fazer o download!'
    
def download_imagem_do_telegram(file_id):
    link = f'https://api.telegram.org/bot{token}/getfile?file_id={file_id}'
    response = requests.get(link)

    if response.status_code == 200:
        file_path = response.json()['result']['file_path']
        link_arquivo = f'https://api.telegram.org/file/bot{token}/{file_path}'

        response = requests.get(link_arquivo)
        with open(f"./imagens/{link_arquivo.split('/')[-1]}", 'wb') as f:
            f.write(response.content)
            return 'Download feito!'
    else:
        return 'Erro ao fazer o download!'
