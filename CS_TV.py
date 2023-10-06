def salvar_cs(dados=''):
    salvar = ''
    separar_vencimento = dados.split('Vencimento: ')
    vencimento = separar_vencimento[1]
    salvar += f'Vencimento: {vencimento[0:19]}\nNome do Cliente: Julio\n'
    separar_usuario = dados.split('login / usuario:&nbsp;')
    usuario = separar_usuario[1]
    fim_usuario = usuario.find('<')
    salvar += f'Login / Usuário: {usuario[0:fim_usuario]}\n'
    separar_senha = dados.split('Senha / password: ')
    senha = separar_senha[1]
    salvar += f'Senha / Password: {senha[0:3]}\n\nDADOS DO SERVIDOR:\nCLARO TV HD\nUrl / IP: csbrasilia1.duckdns.org\nPorta: 32005\nChave DES: 01 02 03 04 05 06 07 08 09 10 11 12 13 14'
    with open('Cs_Tv.txt', 'wt+', encoding='utf8') as arquivo:
        arquivo.write(salvar)


def CS_GOIAS():
    from playwright.sync_api import sync_playwright
    from time import sleep
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=False)
        email_temporario = navegador.new_page()
        email_temporario.set_default_timeout(120000) #Esperar no máximo 2 minutos
        email_temporario.goto('https://pt.emailfake.com/') #Acessar o Site
        print('Acessando Site...')
        pegar_dados_email = str(email_temporario.content())
        pegar_email = pegar_dados_email.split('<span id="email_ch_text">')
        separar_email = pegar_email[1]
        caracteres = separar_email.find('<')
        email = separar_email[0:caracteres]
        print('Gerando E-MAIL aleatório...')
        cs_goias = navegador.new_page()
        # Site oficial do CS Goias https://csgoias.com/
        #cs_goias.goto('http://superpainel.mine.nu/painel/formulario_testes.php?r=SGJtd0pmNXd1TTlzRUNtT25JK0lTallkL1RQVnBTMkFBQXMrWnlsZXEvdz0,') #Teste 48H Cs
        cs_goias.goto('http://csbrasilia1.duckdns.org/painelvix/formulario_testes.php?r=UXVYcWlIdlpuOVVVM1djRzRZWFF2T1lZRUhRcHNHbGxXdlBZVy9rOCtXaz0,')
        print('Acessando Site do Cs...')
        cs_goias.fill('xpath=/html/body/div/div/form/div[1]/input', 'Julio') #Preencher Nome
        cs_goias.fill('xpath=/html/body/div/div/form/div[2]/input', f'{email}') #Preencher Email
        cs_goias.locator('xpath=/html/body/div/div/form/div[3]/div/input').click() #Claro Tv Hd
        print('Preenchendo Dados...')
        cs_goias.locator('xpath=/html/body/div/div/form/div[4]/button').click() #Enviar
        print('Enviando dados da conexão CS TV...')
        sleep(5)
        email_temporario.reload()
        dados = str(email_temporario.content())
        print('Salvando CS TV...')
        salvar_cs(dados)
        print('--------------------------Teste Cs criado com SUCESSO!--------------------------')

cs = int(input('Qual CS deseja?\n[1] Para CS_GOIAS\n[2] Para CS_VIP\n>>> Sua escolha: '))
if cs == 1:
    CS_GOIAS()
elif cs == 2:
    import CS_VIP
