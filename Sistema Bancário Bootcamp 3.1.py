import textwrap

# Função para exibir o menu e obter a opção do usuário
def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


# Função para realizar um depósito
def depositar(saldo, valor, extrato):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor do depósito deve ser maior que zero. @@@")
        return saldo, extrato

    saldo += valor
    extrato += f"Depósito:\tR$ {valor:.2f}\n"
    print("\n=== Depósito realizado com sucesso! ===")
    return saldo, extrato


# Função para realizar um saque
def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor do saque deve ser maior que zero. @@@")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        return saldo, extrato, numero_saques

    if valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite diário permitido. @@@")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato += f"Saque:\t\tR$ {valor:.2f}\n"
    numero_saques += 1
    print("\n=== Saque realizado com sucesso! ===")
    return saldo, extrato, numero_saques


# Função para exibir o extrato
def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if not cpf.isdigit():
        print("\n@@@ CPF inválido! Deve conter apenas números. @@@")
        return

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")


# Função para criar uma nova conta
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if not usuario:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


# Função para listar todas as contas
def listar_contas(contas):
    if not contas:
        print("\n=== Não há contas cadastradas ainda. ===")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print(f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """)
        print("=" * 100)


# Função principal que gerencia o fluxo do programa
def main():
    LIMITE_SAQUES = 3  # Limite de saques por dia
    AGENCIA = "0001"  # Código da agência

    saldo = 0
    limite = 500  # Limite de saque diário
    extrato = ""
    numero_saques = 0  # Contador de saques realizados
    usuarios = []  # Lista de usuários
    contas = []  # Lista de contas

    while True:
        opcao = menu()  # Exibe o menu e recebe a opção do usuário

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1  # Gera o número da nova conta
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Chama a função principal para iniciar o programa
if __name__ == "__main__":
    main()
