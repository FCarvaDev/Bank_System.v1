# Desafio - Sistema Bancário com Python v3
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizartransacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)    

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia    
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
           print("\n|Erro| Você não tem saldo suficiente!")
       
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")   
            return True 
              
        else:
            print("\n|Erro| Operação inválida! O valor informado é inválido.") 
            return False  
        
    def depositar(self, valor):
        if valor > 0:
           self._saldo += valor
           print("Depósito realizado com sucesso!")       
        else:
           print("|Erro| O valor informado é inválido!")
           return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao ["Tipo"] == Saque.__name__])
       
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques 

        if excedeu_limite:
           print("\n|Erro| O valor do saque excede o limite!")

        elif excedeu_saques:
           print("\n|Erro| O limite máximo de saques diários foi excedido!")   

        else:
            return super().sacar(valor)

        return False   
    
    def __str__(self):
        f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []        

    @property
    def transacoes(self):
        return self._transacoes    
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                 "tipo": transacao.__class__.__name__,
                 "valor": transacao.valor,
                 "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),

            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor    
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)    

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu(): 
    menu = """\n 
    ==============================
    ******************************
    ==============================
             CarvBank
    ==============================              
    [1]\tDepositar 
    [2]\tSacar 
    [3]\tExtrato
    [4]\tNovo Usuário
    [5]\tNova Conta
    [6]\tListar Contas 
    [0]\tSair 
    ==============================
    ******************************
    ==============================
    Insira uma operação: """
    return input(textwrap.dedent(menu))

def exibir_extrato(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("|ERRO| Cliente não encontrado!")
            return 
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        print("\n=================== EXTRATO ===================")
        transacoes = conta.historico.transacoes
        
        extrato = ""
        if not transacoes:
            extrato = "Não foi realizada nenhuma movimentação bancária!"
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
        print(extrato)  
        print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
        print("=================================================")

def criar_cliente(clientes):
    cpf = input("Informe seu CPF (somente números): ")
    cliente = filtrar_cliente(cpf, cliente)

    if cliente:
        print("\n|ERRO| CPF já cadastrado!")
        return 
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe seu endereço (logradouro, n° - bairro - cidade/UF): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("CPF cadastrado com sucesso!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None 

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("|ERRO| O cliente não possuí conta!")
        return 
    # FIXME: não permite o cliente a escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n|ERRO| Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor de depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("|ERRO| Cliente não encontrado!")
        return
    valor = float(input("Informe o valor de saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n|ERRO| Usuário não encontrado! Operação de criação de conta encerrado.")
        return 
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")
    


    print("=" * 100)
    print(textwrap.dedent(linha))    

def listar_contas(contas):
    for conta in contas:
        print("=" + 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []


    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
             sacar(clientes)
        

        elif opcao == "3":
            exibir_extrato(clientes)   

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            print("Agradecemos por utilizar nosso sistema bancário! Volte sempre!")
            break    

        else:
            print("|Erro| Operação inválida! Por favor, selecione novamente a operação desejada.")
            
main()        