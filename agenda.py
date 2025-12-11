from datetime import datetime, timedelta

agendamento = []  # onde os agendamentos ficam salvos

# -------------------------------------------------------
# ✅ Função para gerar datas automáticas (SEM DOMINGO)
# -------------------------------------------------------
def gerar_datas_automaticas(dias=30):
    hoje = datetime.now()
    datas = []

    for i in range(dias):
        dia = hoje + timedelta(days=i)

        if dia.weekday() == 6:  # domingo
            continue

        datas.append(dia.strftime("%d/%m/%Y"))

    return datas

# -------------------------------------------------------
# ✅ Função para gerar horários conforme o dia
# -------------------------------------------------------
def gerar_horarios_por_dia(data_escolhida):
    dia = datetime.strptime(data_escolhida, "%d/%m/%Y")
    weekday = dia.weekday()  # 0=seg, ..., 5=sáb, 6=dom

    if weekday == 6:
        return []

    # segunda a sexta → só 18:00
    if weekday in [0, 1, 2, 3, 4]:
        return ["18:00"]

    # sábado
    if weekday == 5:
        return [
            "07:00", "08:45", "09:00", "10:50",
            "13:00", "14:45", "15:00", "17:00"
        ]

    return []
