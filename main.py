from agenda import gerar_datas_automaticas, gerar_horarios_por_dia
from cadastros import carregar_clientes
from servicos_ordens import servico_oferecido

def menu():
    while True:
        print("\n=== Bem vindo a Street Wash ===\n")
        print("\n== Escolha uma Opção ==\n")

        print("1 - cadastrar cliente")
        print("2 - servicos")
        print("3 - agendamentos")
        print("4 - sair\n")
        
        escolha = input("Digite o serviço desejado: ").strip()
            
        if escolha == "1":
            servico_oferecido()
        elif escolha == "2":
            gerar_datas_automaticas()
        elif escolha == "3":
            carregar_clientes()
        elif escolha == "4":
            print("Saindo.. Obrigado por usar Street Wash!")
            break
        else:
            print("Opção invalida!")

