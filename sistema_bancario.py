# =========================
# 💰 Sistema Bancário v2
# =========================

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()

    if filtrar_usuario(cpf, usuarios):
        print("❌ Já existe usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço: ").strip()

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("✅ Usuário criado com sucesso!")


def criar_conta_corrente(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("❌ Usuário não encontrado.")
        return

    contas.append({
        "agencia": "0001",
        "numero_conta": len(contas) + 1,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    })

    print("✅ Conta criada com sucesso!")


def listar_contas_usuario(usuario, contas):
    return [conta for conta in contas if conta["usuario"] == usuario]


def selecionar_conta(usuario, contas):
    contas_usuario = listar_contas_usuario(usuario, contas)

    if not contas_usuario:
        print("❌ Usuário não possui contas.")
        return None

    for conta in contas_usuario:
        print(f"Agência {conta['agencia']} | Conta {conta['numero_conta']}")

    numero = int(input("Informe o número da conta: "))

    for conta in contas_usuario:
        if conta["numero_conta"] == numero:
            return conta

    print("❌ Conta não encontrada.")
    return None


def depositar(conta, /):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print("✅ Depósito realizado.")
    else:
        print("❌ Valor inválido.")


def sacar(*, conta, limite, LIMITE_SAQUES):
    valor = float(input("Informe o valor do saque: "))

    if valor > conta["saldo"]:
        print("❌ Saldo insuficiente.")
    elif valor > limite:
        print("❌ Limite excedido.")
    elif conta["numero_saques"] >= LIMITE_SAQUES:
        print("❌ Número máximo de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print("💸 Saque realizado.")
    else:
        print("❌ Valor inválido.")


def exibir_extrato(conta, /):
    print("\n========== EXTRATO ==========")
    print(conta["extrato"] if conta["extrato"] else "Não foram realizadas movimentações.")
    print(f"Saldo: R$ {conta['saldo']:.2f}")
    print("=============================\n")


# =========================
# Função principal
# =========================
def main():
    menu = """
[u] Criar usuário
[c] Criar conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """

    usuarios = []
    contas = []

    LIMITE_SAQUES = 3
    limite = 500

    while True:
        opcao = input(menu)

        if opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            criar_conta_corrente(usuarios, contas)

        elif opcao in ("d", "s", "e"):
            cpf = input("Informe o CPF: ").strip()
            usuario = filtrar_usuario(cpf, usuarios)

            if not usuario:
                print("❌ Usuário não encontrado.")
                continue

            conta = selecionar_conta(usuario, contas)
            if not conta:
                continue

            if opcao == "d":
                depositar(conta)

            elif opcao == "s":
                sacar(conta=conta, limite=limite, LIMITE_SAQUES=LIMITE_SAQUES)

            elif opcao == "e":
                exibir_extrato(conta)

        elif opcao == "q":
            print("👋 Sistema encerrado.")
            break

        else:
            print("⚠️ Opção inválida.")


main()
