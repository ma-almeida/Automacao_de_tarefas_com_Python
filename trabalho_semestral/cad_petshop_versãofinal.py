import requests 
import customtkinter 
from tkinter import messagebox 
import mysql.connector

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",         
    user="root",       
    password="",     
    database="cad_petshop1"  
)
cursor = conexao.cursor()

# Configuração da interface
customtkinter.set_appearance_mode('system') #Define a cor dos sistema de acordo com o sistema operacional.
customtkinter.set_default_color_theme('blue') #Define a cor padrão da interface - como botões, fundo, etc.

# Variáveis globais são usadas para armazenar dados entre funções por todo o código
confirmacao = None # Variável para armazenar a confirmação de cadastro
mensagem_confirmação = None # Variável para armazenar a mensagem de erro
cliente_id_atual = None # Variável para armazenar o ID do cliente atual
pet_id_atual = None # Variável para armazenar o ID do pet atual

# Funções auxiliares
def focus_next(event): # Função para mover o foco para o próximo widget
    event.widget.tk_focusNext().focus() 
    return "break" #Cancela o evento padrão do widget

def buscar_endereco():
    cep = cep_entry.get().strip()
    if len(cep) == 8 and cep.isdigit():
        url = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" not in dados:
                cep_entry.delete(0, customtkinter.END)
                logradouro.delete(0, customtkinter.END)
                bairro.delete(0, customtkinter.END)
                cidade.delete(0, customtkinter.END)

                cep_entry.insert(0, dados.get('cep', ''))
                logradouro.insert(0, dados.get('logradouro', ''))
                bairro.insert(0, dados.get('bairro', ''))
                cidade.insert(0, dados.get('localidade', ''))
            else:
                messagebox.showerror('Erro', "CEP não encontrado.")
        else:
            messagebox.showerror('Erro', "Erro ao buscar o CEP.")
    else:
        messagebox.showerror('Aviso', "CEP inválido. Digite 8 números.")

# Função para cadastrar cliente
def cadastrar_cliente():
    global mensagem_confirmação, cliente_id_atual

    # Primeiro obtém todos os valores
    nome_valor = nome.get().strip()
    cpf_valor = cpf.get().strip()
    telefone_valor = telefone.get().strip()
    email_valor = email.get().strip()
    cep_valor = cep_entry.get().strip()
    logradouro_valor = logradouro.get().strip()
    numero_valor = numero.get().strip()
    bairro_valor = bairro.get().strip()
    cidade_valor = cidade.get().strip() #Get() obtém o valor do campo de entrada, strip() remove espaços em branco no início e no final da string

    # Primeiro verifica se todos os campos obrigatórios estão preenchidos
    if not all([nome_valor, cpf_valor, telefone_valor, cep_valor, logradouro_valor, numero_valor, bairro_valor, cidade_valor]):
        if mensagem_confirmação is not None:
            mensagem_confirmação.destroy()
        mensagem_confirmação = customtkinter.CTkLabel(janela_1, 
            text="Preencha todos os campos obrigatórios!", text_color="red")
        mensagem_confirmação.pack(pady=10)
        return #Retorna para a função sem executar o restante do código

    # Depois verifica o formato do CPF
    if len(cpf_valor) != 11 or not cpf_valor.isdigit():
        if mensagem_confirmação is not None:
            mensagem_confirmação.destroy()
        mensagem_confirmação = customtkinter.CTkLabel(janela_1, 
            text="CPF deve conter exatamente 11 dígitos!", text_color="red")
        mensagem_confirmação.pack(pady=10)
        return
    
    # Depois verifica o formato do telefone
    telefone_valor = telefone.get().strip()
    if len(telefone_valor) != 11 or not telefone_valor.isdigit():
        if mensagem_confirmação is not None: #None é um valor nulo, ou seja, não existe nada armazenado na variável
            mensagem_confirmação.destroy() #Remove o widget de mensagem anterior, se já existir
        mensagem_confirmação = customtkinter.CTkLabel(janela_1, 
            text="Telefone deve conter 11 dígitos!", text_color="red")
        mensagem_confirmação.pack(pady=10)
        return

    try:
        # Verificar se CPF já existe
        cursor.execute("SELECT id_cliente FROM tbl_clientes WHERE cpf_cliente = %s", (cpf_valor,))
        if cursor.fetchone():
            if mensagem_confirmação is not None:
                mensagem_confirmação.destroy()
            mensagem_confirmação = customtkinter.CTkLabel(janela_1, text="CPF já cadastrado!", text_color="red")
            mensagem_confirmação.pack(pady=10)
            return


        # Inserir cliente
        sql = """INSERT INTO tbl_clientes 
                (nome_cliente, cpf_cliente, telefone_cliente, email_cliente, cep, logradouro, numero, bairro, cidade) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = (nome_valor, cpf_valor, telefone_valor, email_valor, cep_valor, 
                  logradouro_valor, numero_valor, bairro_valor, cidade_valor)
        
        cursor.execute(sql, valores)
        cliente_id_atual = cursor.lastrowid
        conexao.commit() #commit() salva as alterações no banco de dados

        if mensagem_confirmação is not None:
            mensagem_confirmação.destroy()

        mensagem_confirmação = customtkinter.CTkLabel(janela_1, text="Cliente cadastrado com sucesso!", text_color="green")
        mensagem_confirmação.pack(pady=10)

        # Limpar campos
        nome.delete(0, 'end')
        cpf.delete(0, 'end')
        telefone.delete(0, 'end')
        email.delete(0, 'end')
        cep_entry.delete(0, 'end')
        logradouro.delete(0, 'end')
        numero.delete(0, 'end')
        bairro.delete(0, 'end')
        cidade.delete(0, 'end')


    except mysql.connector.Error as erro:
        if mensagem_confirmação is not None:
            mensagem_confirmação.destroy()
            
        mensagem_confirmação = customtkinter.CTkLabel(janela_1, 
            text=f"Erro ao cadastrar cliente: {erro}", text_color="red")
        mensagem_confirmação.pack(pady=10)
         #except mysql.connector.Error as erro: captura o erro caso ocorra um erro de conexão com o banco de dados

# Função para abrir janela de pets
def abrir_janela_pets():
    if cliente_id_atual is None:
        messagebox.showerror("Erro", "Você precisa cadastrar um cliente primeiro!")
        return
    
    global janela_pets
    janela_pets = customtkinter.CTkToplevel(janela_1)
    janela_pets.title('Cadastro de Pets')
    janela_pets.geometry('500x300')
    janela_pets.configure(fg_color='#FFCCCC')

    janela_pets.attributes('-topmost', True)  # Mantém no topo
    janela_pets.focus_force()  # Força o foco
    janela_pets.lift()  # Traz para frente
    janela_pets.after(200, lambda: janela_pets.attributes('-topmost', False)) #Remove o foco da janela permitindo que ela possa ser minimizada
    texto = customtkinter.CTkLabel(janela_pets, text='Cadastro de Pets', font=('Arial', 16, 'bold'))
    texto.pack(padx=10, pady=10)

    global nome_pet, porte_pet, raca_pet, idade_pet, observacao_pet
    nome_pet = customtkinter.CTkEntry(janela_pets, placeholder_text='Nome do Pet*')
    nome_pet.pack(padx=10, pady=5)

    porte_pet = customtkinter.CTkEntry(janela_pets, placeholder_text='Porte do Pet*')
    porte_pet.pack(padx=10, pady=5)

    raca_pet = customtkinter.CTkEntry(janela_pets, placeholder_text='Raça do Pet*')
    raca_pet.pack(padx=10, pady=5)

    idade_pet = customtkinter.CTkEntry(janela_pets, placeholder_text='Idade do Pet*')
    idade_pet.pack(padx=10, pady=5)

    observacao_pet = customtkinter.CTkEntry(janela_pets, placeholder_text='Observação do Pet')
    observacao_pet.pack(padx=10, pady=5)

    frame_botoes_pets = customtkinter.CTkFrame(janela_pets, fg_color='transparent')
    frame_botoes_pets.pack(pady=10)

    botao_salvar_pet = customtkinter.CTkButton(frame_botoes_pets, text='Cadastrar Pet', command=salvar_pet)
    botao_salvar_pet.pack(side='left', padx=10)

    botao_servicos = customtkinter.CTkButton(frame_botoes_pets, text='Cadastrar Serviços', command=abrir_janela_servicos)
    botao_servicos.pack(side='left', padx=10)

    nome_pet.bind("<Return>", focus_next)
    porte_pet.bind("<Return>", focus_next)
    raca_pet.bind("<Return>", focus_next)
    idade_pet.bind("<Return>", focus_next)
    observacao_pet.bind("<Return>", focus_next)

# Função para salvar pet
def salvar_pet():
    global confirmacao, pet_id_atual
    
    nome_valor = nome_pet.get().strip()
    porte_valor = porte_pet.get().strip()
    raca_valor = raca_pet.get().strip()
    idade_valor = idade_pet.get().strip()
    observacao_valor = observacao_pet.get().strip()

    if confirmacao is not None:
        confirmacao.destroy()

    if not all([nome_valor, porte_valor, raca_valor, idade_valor]):
        confirmacao = customtkinter.CTkLabel(janela_pets, text="Preencha todos os campos obrigatórios!", text_color="red")
        confirmacao.pack(pady=10)
        return

#try contém o código que pode gerar erro, caso ocorra um erro, o except executa o código dentro dele
    try:
        sql = """INSERT INTO tbl_pet 
                (nome_pet, porte_pet, raca_pet, idade_pet, observacao_pet, fk_cliente_pet) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (nome_valor, porte_valor, raca_valor, idade_valor, observacao_valor, cliente_id_atual)
        
        cursor.execute(sql, valores)
        pet_id_atual = cursor.lastrowid
        conexao.commit()

        confirmacao = customtkinter.CTkLabel(janela_pets, text="Pet cadastrado com sucesso!", text_color="green")
        confirmacao.pack(pady=10)

        nome_pet.delete(0, 'end')
        porte_pet.delete(0, 'end')
        raca_pet.delete(0, 'end')
        idade_pet.delete(0, 'end')
        observacao_pet.delete(0, 'end') #Limpa os campos após o cadastro

    except mysql.connector.Error as erro:
        confirmacao = customtkinter.CTkLabel(janela_pets, 
            text=f"Erro ao cadastrar pet: {erro}", text_color="red")
        confirmacao.pack(pady=10)

# Função para abrir janela de serviços
def abrir_janela_servicos():
    if pet_id_atual is None:
        messagebox.showerror("Erro", "Você precisa cadastrar um pet primeiro!")
        return
    
    global janela_servicos
    janela_servicos = customtkinter.CTkToplevel(janela_pets)
    janela_servicos.title('Serviços Pets')
    janela_servicos.geometry('500x300')
    janela_servicos.configure(fg_color='#FFCCCC')

    janela_servicos.attributes('-topmost', True)  # Mantém no topo
    janela_servicos.focus_force()  # Força o foco
    janela_servicos.lift()  # Traz para frente
    janela_servicos.after(200, lambda: janela_servicos.attributes('-topmost', False)) #Remove o foco da janela permitindo que ela possa ser minimizada
    
    texto = customtkinter.CTkLabel(janela_servicos, text='Cadastro de Serviços', font=('Arial', 16, 'bold'))
    texto.pack(padx=10, pady=10)

    global entry_servico, entry_valor
    entry_servico = customtkinter.CTkEntry(janela_servicos, placeholder_text="Tipo de Serviço*")
    entry_servico.pack(pady=5)

    entry_valor = customtkinter.CTkEntry(janela_servicos, placeholder_text="Valor*")
    entry_valor.pack(pady=5)

    botao_salvar_servico = customtkinter.CTkButton(janela_servicos, text="Cadastrar Serviço", command=salvar_servico)
    botao_salvar_servico.pack(pady=10)

    entry_servico.bind("<Return>", focus_next)
    entry_valor.bind("<Return>", focus_next)

# Função para salvar serviço
def salvar_servico():
    global confirmacao
    
    servico = entry_servico.get().strip()
    valor = entry_valor.get().strip()

    if not all([servico, valor]):
        if confirmacao is not None:
            confirmacao.destroy()
        confirmacao = customtkinter.CTkLabel(janela_servicos, text="Preencha todos os campos obrigatórios!", text_color="red")
        confirmacao.pack(pady=10)
        return

    valor_ajustado = valor.replace(",", ".")
    try:
        valor_float = float(valor_ajustado)
    except ValueError:
        if confirmacao is not None:
            confirmacao.destroy()
        confirmacao = customtkinter.CTkLabel(janela_servicos, text="Valor deve ser um número válido!", text_color="red")
        confirmacao.pack(pady=10)
        return

    try:
        sql = """INSERT INTO tbl_servicos 
                (tipo_servico, valores_servico, fk_servico_pet) 
                VALUES (%s, %s, %s)"""
        valores = (servico, valor_float, pet_id_atual)
        
        cursor.execute(sql, valores)
        conexao.commit()

        if confirmacao is not None:
            confirmacao.destroy()
        
        confirmacao = customtkinter.CTkLabel(janela_servicos, text="Serviço cadastrado com sucesso!", text_color="green")
        confirmacao.pack(pady=10)

        entry_servico.delete(0, 'end')
        entry_valor.delete(0, 'end')

    except mysql.connector.Error as erro:
        if confirmacao is not None:
            confirmacao.destroy()
            
        confirmacao = customtkinter.CTkLabel(janela_servicos, 
            text=f"Erro ao cadastrar serviço: {erro}", text_color="red")
        confirmacao.pack(pady=10)

# Janela principal
janela_1 = customtkinter.CTk()
janela_1.title('Cadastro de Clientes')
janela_1.geometry('500x300')
janela_1.configure(fg_color="#FFCCCC")

texto = customtkinter.CTkLabel(janela_1, text="Cadastro de Clientes", font=("Arial", 16, "bold")) 
texto.pack(padx=10, pady=10)

# Campos do formulário de clientes
nome = customtkinter.CTkEntry(janela_1, placeholder_text='Nome do Cliente*')
nome.pack(padx=10, pady=5)

cpf = customtkinter.CTkEntry(janela_1, placeholder_text='CPF*')
cpf.pack(padx=10, pady=5)

telefone = customtkinter.CTkEntry(janela_1, placeholder_text='Telefone*')
telefone.pack(padx=10, pady=5)

email = customtkinter.CTkEntry(janela_1, placeholder_text='Email')
email.pack(padx=10, pady=5)

cep_entry = customtkinter.CTkEntry(janela_1, placeholder_text='CEP*')
cep_entry.pack(padx=10, pady=5)

botao_buscar = customtkinter.CTkButton(janela_1, text="Buscar Endereço", command=buscar_endereco)
botao_buscar.pack(padx=10, pady=5)

logradouro = customtkinter.CTkEntry(janela_1, placeholder_text='Logradouro*')
logradouro.pack(padx=10, pady=5)

numero = customtkinter.CTkEntry(janela_1, placeholder_text='Número*')
numero.pack(padx=10, pady=5)

bairro = customtkinter.CTkEntry(janela_1, placeholder_text='Bairro*')
bairro.pack(padx=10, pady=5)

cidade = customtkinter.CTkEntry(janela_1, placeholder_text='Cidade*')
cidade.pack(padx=10, pady=5)

frame_botoes = customtkinter.CTkFrame(janela_1, fg_color='transparent')
frame_botoes.pack(pady=10)

botao_cadastrar_cliente = customtkinter.CTkButton(frame_botoes, text='Cadastrar Cliente', command=cadastrar_cliente)
botao_cadastrar_cliente.pack(side='left', padx=10)

botao_cadastrar_pet = customtkinter.CTkButton(frame_botoes, text='Cadastrar Pet', command=abrir_janela_pets)
botao_cadastrar_pet.pack(side='left', padx=10)

# Configuração de eventos
nome.bind("<Return>", focus_next)
cpf.bind("<Return>", focus_next)
telefone.bind("<Return>", focus_next)
email.bind("<Return>", focus_next)
cep_entry.bind("<Return>", focus_next)
logradouro.bind("<Return>", focus_next)
numero.bind("<Return>", focus_next)
bairro.bind("<Return>", focus_next)
cidade.bind("<Return>", focus_next)

# Loop principal
janela_1.mainloop() # Mantém a janela aberta

# Fechar conexão ao sair
cursor.close()
conexao.close()