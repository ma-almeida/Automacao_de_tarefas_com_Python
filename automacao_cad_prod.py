import pyautogui
pyautogui.FAILSAFE = True # Se o mouse for para o canto superior esquerdo da tela, o programa para de rodar. 
import time
pyautogui.PAUSE = 0.5 # Pausa de 0.5 segundo entre cada ação

# pyautogui.click -> clicar em algum lugar da tela
# pyautogui.write -> escrever algo na tela
# pyautogui.press -> pressionar uma tecla do teclado 
# pyautogui.hotkey _> pressionar uma combinação de teclas do teclado (ex. pyautogui.hotkey('ctrl', 'c') para copiar)
# pyautogui.PAUSE = 1 -> adicionar uma pausa de 1 segundo entre cada ação para evitar que o computador fique muito rápido e não consiga acompanhar as ações do pyautogui. Precisa ser em letra maiúscula 

# Passo 1: Entrar no sistema da empresa - https://dlp.hashtagtreinamentos.com/python/intensivao/login
# abrir o chrome 
pyautogui.press ('win')
pyautogui.write ('google')
pyautogui.press ('enter')

# digitar o site 
pyautogui.write ('https://dlp.hashtagtreinamentos.com/python/intensivao/login')
pyautogui.press ('enter')

time.sleep(3)
#Esperar 3 segundos para o site carregar. Irá esperar 3 segundos apenas nesse momento especifico, depois não irá esperar mais. 

# Passo 2: Fazer login
# preencher email
pyautogui.click (x=740, y=459) #clicar no campo de login 
pyautogui.write ('marcella.a.l@gmail.com') 

# preencher senha 
pyautogui.press ('tab') #pressionar tab para ir para o próximo campo 
pyautogui.write ('123456')

# botão logar 
pyautogui.press ('tab')
pyautogui.press ('enter')

#espera de 3 segundos para o site carregar
time.sleep(3)

# Passo 3: Importar a base de dados 
import pandas 

tabela = pandas.read_csv ('produtos.csv') #read = ler um arquivo

print (tabela)

# Passo 4: Cadastrar 1 produto 
# se fosse para cada coluna seria: for coluna in tabela.columns: para cada coluna da minha tabela.

for linha in tabela.index: # para cada linha da minha tabela. Selecionar o que eu quero que ele faça (for) e apertar tab para incluir no for.
    pyautogui.click (x=927, y=333) #clicar no botão de cadastrar produto 

    codigo = tabela.loc [linha, 'codigo'] #loc = localizar o que eu quero na tabela. Precisa ser o mesmo nome do arquivo. 
    pyautogui.write (codigo) #escrever o código do produto no campo produto 

    #toda lista de coisas no python fuca entre colchetes.

    pyautogui.press ('tab') #pressionar tab para ir para o próximo campo
    marca = tabela.loc [linha, 'marca']
    pyautogui.write (marca)

    pyautogui.press ('tab') #pressionar tab para ir para o próximo campo
    tipo = tabela.loc [linha, 'tipo']
    pyautogui.write (tipo)

    pyautogui.press ('tab') #pressionar tab para ir para o próximo campo
    categoria = str (tabela.loc [linha, 'categoria']) # precisa ser string porque é um número. Senão, ele vai colocar o número inteiro e não vai reconhecer porque o pyautoguinão reconhece número inteiro. 
    pyautogui.write (categoria)

    pyautogui.press ('tab') #pressionar tab para ir para o próximo campo
    preco_unitario = str (tabela.loc [linha, 'preco_unitario']) #str = string/texto. 
    pyautogui.write (preco_unitario)

    pyautogui.press ('tab') #pressionar tab para ir para o próximo campo
    custo = str (tabela.loc [linha, 'custo'])
    pyautogui.write (custo)

    pyautogui.press ('tab') #pressionar tab para ir para o próximo campo
    obs = str (tabela.loc [linha, 'obs'])

    if obs != 'nan': #!= diferente de. Se o valor for diferente de nan, ele vai escrever o que está na tabela.  
        pyautogui.write (obs)

    pyautogui.press ('tab') #passou para o botão enviar 
    pyautogui.press ('enter')

    pyautogui.scroll (10000) #subir a tela para cadastrar um novo produto. Ajustar o número de acordo com a necessidade

# Passo 5: Repetir todos os produtos 


# pyautogui: é uma biblioteca que permite controlar o mouse e o teclado do computador, permitindo automatizar tarefas repetitivas.

# pandas: é uma biblioteca de manipulação e análise de dados, que fornece estruturas de dados flexíveis e eficientes para trabalhar com dados tabulares.

# para parar um automação levar o mouse para o canto superior esquerdo da tela. 

# nan = not a number. Representa um valor ausente ou indefinido em um conjunto de dados. 