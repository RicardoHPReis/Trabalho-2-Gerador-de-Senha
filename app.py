import datetime as d
import hashlib as h
import random as r
import time as t
import pytz
import os

SALT:str = "6394"
horario_local = pytz.timezone('America/Sao_Paulo') 


def titulo():
    print("--------------------------------")
    print("Gerador de Senha - APP")
    print("--------------------------------\n")
    
    
def titulo_acesso():
    print("--------------------------------")
    print("Acesso do Usuário - APP")
    print("--------------------------------\n")


def ler_arquivo_texto() -> list:
    list_usuarios = []
    with open("dados_app.txt", 'r') as arquivo:
        for n, linha in enumerate(arquivo):
            registro = linha.split(' ')
            list_usuarios.append({"Usuario": registro[0],
                            "Senha_semente": registro[1],
                            "Senha_local": registro[2].replace("\n","") })
    return list_usuarios


def gerar_arquivo_texto(texto:str) -> None:
    with open("dados_app.txt", "a") as arquivo:
        arquivo.write(texto + "\n")



def pesquisar(list_usuarios:list, texto:str):
    for i in list_usuarios:
        if any(texto in v for k, v in i.items()):
            return i
    return {}


def hash_senha(senha:str, salt:str="") -> str:
    return h.sha256((senha + salt).encode(), usedforsecurity=True).hexdigest()


def criar_usuario() -> None:
    nome_usuario = input("Digite o nome do usuário: ")
    #salt = "{:04}".format(r.randint(0,9999))
    salt = str(SALT)
    salt_hash = hash_senha(salt)
    senha_principal = hash_senha(input("Digite a senha semente: ").strip())
    senha_principal_hash = hash_senha(senha_principal, salt_hash)
    senha_local_hash = hash_senha(input("Digite a senha local: ").strip())
    gerar_arquivo_texto(nome_usuario + " " + senha_principal_hash + " " + senha_local_hash)
    

def acessar_senhas() -> None:
    tentativas:int = 3
    dados = ler_arquivo_texto()
    while tentativas != 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        nome_usuario = input("Digite o nome do usuário: ")
        senha_local_hash = hash_senha(input("Digite a senha local: ").strip())
        pesquisa = pesquisar(dados, nome_usuario)
        if nome_usuario == pesquisa['Usuario'] and senha_local_hash == pesquisa['Senha_local']:
            entrar_usuario(pesquisa)
            break
        else:
            tentativas -= 1
            print(f'O usuário ou a senha estão incorretos! Há {tentativas} tentativas restantes.')
            t.sleep(2)


def gerar_token(dados:dict) -> None:   
    while (True):
        os.system('cls' if os.name == 'nt' else 'clear')
        lista_tokens = []
        horario = d.datetime.now(horario_local)
        horario_hash = horario.strftime("%d%m%Y%H%M")
        horario_print = horario.strftime("%d/%m/%Y %H:%M:%S")
        token = hash_senha(dados['Senha_semente'] + horario_hash)
        #lista_tokens.append(token)

        for i in range(0, 5):
            token = hash_token(token)
            lista_tokens.append(token)
        lista_tokens.reverse()
        
        print(horario_print)
        print(lista_tokens)
        t.sleep(1)


def hash_token(codigo:str):
    dado_hash = h.sha256(codigo.encode()).hexdigest()
    otp = "{:06}".format(int(dado_hash[14:20], 16))
    return otp


def entrar_usuario(dados:dict) -> None:
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo_acesso()
        print('1) Gerar token.')
        print('2) Sair.')
        opcao = int(input("Escolha uma opção: "))
        match opcao:
            case 1:
                gerar_token(dados)
                input("Digite algo para continuar... ")
            case 2:
                break
            case _:
                print('A escolha precisa estar nas opções acima!')
                t.sleep(2)


def gerador_senha():    
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print('1) Criar usuário.')
        print('2) Entrar como usuário.')
        print('3) Sair.')
        opcao = int(input("Escolha uma opção: "))
        match opcao:
            case 1:
                criar_usuario()
                input("Digite algo para continuar... ")
            case 2:
                acessar_senhas()
                input("Digite algo para continuar... ")
            case 3:
                break
            case _:
                print('A escolha precisa estar nas opções acima!')
                t.sleep(2)


def main():
    gerador_senha()


if __name__ == "__main__":
    main()