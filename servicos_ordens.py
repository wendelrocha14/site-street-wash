def servico_oferecido():
    print("\n--- Nossos Serviços ---\n")
  
    lista_servicos = {
        "Lavagem Fast": 60,
        "Lavagem Standard": 70,
        "Lavagem Premium": 110,
        "Moto": 30,
        "Vitrificação": 130,
        "Polimento": 180
    }

    for nome, valor in lista_servicos.items():
        print(f"{nome}: R$ {valor}")

    input("\nPressione ENTER para voltar ao menu...")
