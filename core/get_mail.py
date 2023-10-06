try:
    import requests
except:
     import os 
     os.system("pip install requests")
     import requests
import json
from core.token_parser import *
from core.gen_email import *
from core.text_parser import *


def formatar(txt):
    pos = str(txt).find('\n')
    return txt[0:pos]


def salvar_cs_vip(gmail: str, id_da_mensagem: str):
    #site oficial do Cs Vip na construção deste código https://testecs48horas.vip/
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=False)
        emailnator = navegador.new_page()
        emailnator.set_default_timeout(120000)
        emailnator.goto(f'https://www.emailnator.com/inbox/{gmail}/{id_da_mensagem}')
        all_vencimento = emailnator.locator('xpath=//*[@id="root"]/div/section/div/div/div[3]/div/div/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li/table/tbody/tr[1]/td/table/tbody/tr[7]/td[2]/span').inner_text()
        pos_vencimento = all_vencimento.find(' ')
        vencimento = all_vencimento[0:pos_vencimento - 1]
        usuario = emailnator.locator('xpath=//*[@id="root"]/div/section/div/div/div[3]/div/div/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/span').inner_text()
        senha = emailnator.locator('xpath=//*[@id="root"]/div/section/div/div/div[3]/div/div/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li/table/tbody/tr[1]/td/table/tbody/tr[3]/td[2]/span').inner_text()
        all_ip = formatar(emailnator.locator('xpath=//*[@id="root"]/div/section/div/div/div[3]/div/div/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li/table/tbody/tr[1]/td/table/tbody/tr[4]/td[2]/span').inner_text())
        pos_ip = all_ip.find(':')
        ip = all_ip[pos_ip+2:]
        pos_servidor = all_ip.find(':')
        servidor = all_ip[0:pos_servidor]
        all_porta = formatar(emailnator.locator('xpath=//*[@id="root"]/div/section/div/div/div[3]/div/div/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li/table/tbody/tr[1]/td/table/tbody/tr[5]/td[2]/span').inner_text())
        pos_porta = all_porta.find(':')
        porta = all_porta[pos_porta+2:]
        chave_des = emailnator.locator('xpath=//*[@id="root"]/div/section/div/div/div[3]/div/div/div[2]/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/ul/li/table/tbody/tr[1]/td/table/tbody/tr[6]/td[2]/span').inner_text()
        print('Salvando CS TV...')
        with open('Cs_Tv.txt', 'wt+', encoding='utf8') as arquivo:
            cs_tv = f'Vencimento: {vencimento}\nNome do Cliente: Julio\nLogin / Usuário: {usuario}\nSenha / Password: {senha}\n\nDADOS DO SERVIDOR:\n{servidor}\nUrl / Ip: {ip}\nPorta: {porta}\nChave DES: {chave_des}'
            arquivo.write(cs_tv)
        print('--------------------------Teste Cs criado com SUCESSO!--------------------------')
        exit()


def gerar_cs_vip(gmail: str):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=False)
        cs_vip = navegador.new_page()
        cs_vip.goto('http://teste.ddns.me/painel/cadtest.php?r=VlZaa1UyUkhSbGhPUkRBOQ==')
        print('Acessando Site do Cs...')
        cs_vip.set_default_timeout(120000)
        cs_vip.fill('xpath=//*[@id="nome"]', 'Julio') # Colocando Usuário
        cs_vip.fill('xpath=//*[@id="email"]', gmail) # Colocando gmail fake
        print('Preenchendo Dados...')
        cs_vip.locator('xpath=//*[@id="FormLogin"]/div[5]/div/button').click() # Botão para gerar Teste Cs
        print('Enviando dados da conexão CS TV...')



def get_email_response():
    print("Gerando endereço Gmail.....")
    print("Por favor aguarde :)")
    data_cookie = json.loads(json.dumps(get_cookie()))
    xsrf_token = str(data_cookie['XSRF-TOKEN']).replace('%3D', "=")
    session_token = data_cookie['gmailnator_session']
    burp0_url = "https://www.emailnator.com:443/message-list"
    email = gen_email()
    burp0_cookies = {"XSRF-TOKEN": f"{xsrf_token}",
                     "gmailnator_session": f"{session_token}"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json",
                     "X-Xsrf-Token": f"{xsrf_token}", "Origin": "https://www.emailnator.com", "Referer": "https://www.emailnator.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    burp0_json = {"email": f"{email}"}
    print(f'Email : {email}')
    print('\n\nAguardando Mensagem........')
    gerar_cs_vip(email)
    while True:
        response = requests.post(burp0_url, headers=burp0_headers,
                                 cookies=burp0_cookies, json=burp0_json).json()
        messges_id = response['messageData']
        total_messeges = len(messges_id)
        for i in range(total_messeges):

            if len(str(messges_id[i]['messageID'])) > 12:
                messges_id_base = messges_id[i]['messageID']
                with open('temp_id.txt', 'r') as read_file:
                    if messges_id_base not in str(read_file.readlines()):
                        print(f'Dados da conexão CS Recebidos!')
                        salvar_cs_vip(email, messges_id[1]['messageID'])
                        with open('temp_id.txt','a') as w:
                             w.write(messges_id_base+"\n")
                             w.close()
                        subject_text = messges_id[i]['subject']
                        from_email = messges_id[i]['from']
                        burp0_url_email = "https://www.emailnator.com:443/message-list"
                        burp0_json_email = {"email": f"{email}",
                                            "messageID": f"{messges_id_base}"}
                        message = requests.post(
                            burp0_url_email, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json_email)
                        with open('index.html', 'a+', encoding='utf-8') as w:
                            if str(response) not in str(w.readlines()):

                                w.write(message.text+"\n")
                            w.close()
