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
    print("Gerador de Senha - Servidor")
    print("--------------------------------\n")
    
    
def titulo_acesso():
    print("--------------------------------")
    print("Acesso do Usuário - Servidor")
    print("--------------------------------\n")


def ler_arquivo_texto() -> list:
    list_usuarios = []
    with open("dados_servidor.txt", 'r') as arquivo:
        for n, linha in enumerate(arquivo):
            registro = linha.split(' ')
            list_usuarios.append({"Usuario": registro[0],
                            "Salt": registro[1],
                            "Senha_semente": registro[2],
                            "Senha_local": registro[3].replace("\n","") })
    return list_usuarios


def gerar_arquivo_texto(texto:str) -> None:
    with open("dados_servidor.txt", "a") as arquivo:
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
    senha_principal_hash = hash_senha(input("Digite a senha semente: ").strip())
    senha_local_hash = hash_senha(input("Digite a senha local: ").strip())
    gerar_arquivo_texto(nome_usuario + " " + salt_hash + " " + senha_principal_hash + " " + senha_local_hash)
    

def acessar_senhas() -> None:
    tentativas:int = 3
    dados = ler_arquivo_texto()
    while tentativas != 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        nome_usuario = input("Digite o nome do usuário: ")
        senha_local_hash = hash_senha(input("Digite a senha local: ").strip())
        pesquisa = pesquisar(dados, nome_usuario)
        if pesquisa != {} and (nome_usuario == pesquisa['Usuario'] and senha_local_hash == pesquisa['Senha_local']):
            entrar_usuario(pesquisa)
            break
        else:
            tentativas -= 1
            print(f'O usuário ou a senha estão incorretos! Há {tentativas} tentativas restantes.')
            t.sleep(2)


def verificar_token(dados:dict, h_hash:str, num_tokens:int) -> None:   
    tentativas:int = 3
    token_correto:bool = False
    while tentativas != 0:
        lista_tokens = []
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        token_app = input("Digite o token do APP: ").strip()
        horario = d.datetime.now(horario_local)
        horario_hash = horario.strftime("%d%m%Y%H%M")
        senha_conjunta = hash_senha(dados['Senha_semente'], dados['Salt'])
        token = hash_senha(senha_conjunta + horario_hash)

        if h_hash != horario_hash:
            num_tokens = 5

        for i in range(0, num_tokens):
            token = hash_token(token)
            lista_tokens.append(token)
        
        for i in range(len(lista_tokens)):
            if token_app == lista_tokens[i]:
                token_correto = True
                num_tokens = i
                lista_tokens = lista_tokens[:i]
                break
        
        if token_correto:
            print("Usuário verificado!")
            print(f"Chaves restantes: {lista_tokens}")
            break
        else:
            tentativas -= 1
            print(f'O token está incorreto! Há {tentativas} tentativas restantes.')
            t.sleep(2)
    return horario_hash, num_tokens


def hash_token(codigo:str):
    dado_hash = h.sha256(codigo.encode()).hexdigest()
    otp = "{:06}".format(int(dado_hash[14:20], 16))
    return otp


def entrar_usuario(dados:dict) -> None:
    num_tokens = 5
    horario_hash = ""
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo_acesso()
        print('1) Verificar token.')
        print('2) Sair.')
        opcao = int(input("Escolha uma opção: "))
        match opcao:
            case 1:
                horario_hash, num_tokens = verificar_token(dados, horario_hash, num_tokens)
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
        print('1) Criar usuários.')
        print('2) Verificar como usuário.')
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