# Desafio - Sistema Bancário com Python

menu = """" 

==============================
******************************
==============================
            CarvBank
==============================              

        [1] Depositar 
        [2] Sacar 
        [3] Extrato 
        [0] Sair 

==============================
******************************
==============================

Insira uma operação: """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe um valor para depositar: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("|Erro| O valor informado é inválido!")

    elif opcao == "2":
        valor = float(input("Informe um valor para sacar: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("|Erro| Você não tem saldo suficiente!")

        elif excedeu_limite:
            print("|Erro| O valor do saque excede o limite!")

        elif excedeu_saques:
            print("|Erro| O limite máximo de saques diários foi excedido!")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("|Erro| O valor informado é inválido!")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("Não foi realizada nenhuma movimentação bancária." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "0":
        break

    else:
        print("|Erro| Operação inválida! Por favor, selecione novamente a operação desejada.")