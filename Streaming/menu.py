from usuario import User

def menu():
    usuarios = []  # lista de instâncias User
    logado = None  # guarda o usuário logado

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Signup")
        print("2 - Login")
        print("3 - Ver usuários")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")

            u = User()
            token = u.sign(nome, senha)
            if token:
                usuarios.append(u)
                print(f"✅ Usuário {nome} cadastrado com sucesso!")

        elif opcao == "2":
            nome = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")

            for u in usuarios:
                if u.user == nome and u.password == senha:
                    logado = u
                    print(f"🔑 Login bem-sucedido! Bem-vindo {nome}")
                    break     
            else:
                print("❌ Usuário ou senha incorretos.")

        elif opcao == "3":
            if not usuarios:
                print("Nenhum usuário cadastrado ainda.")
            else:
                print("=== Lista de usuários cadastrados ===")
                for u in usuarios:
                    print(f"- {nome}")

        # Sair
        elif opcao == "4":
            print("👋 Saindo do sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()
