from flask import Flask, render_template, request, redirect
from cadastros import clientes, salvar_clientes
from agenda import gerar_datas_automaticas, gerar_horarios_por_dia, agendamento

app = Flask(__name__)

# Valores dos serviços - TABELA ÚNICA
PRECOS_SERVICOS = {
    "Lavagem De Manutenção": 60,
    "Lavagem Detalhada Premium": 70,
    "Moto": 30
}

# Valores extras
PRECOS_EXTRAS = {
    "Removedor de Piche": 10,
    "Cera Líquida Premium": 50,
    "Nenhum": 0
}

# Dias ocupados (para quando quiser usar depois)
DIAS_OCUPADOS = set()


# Página inicial
@app.route("/")
def home():
    return render_template("index.html")


# Cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]

        novo = {"nome": nome, "telefone": telefone}
        clientes.append(novo)
        salvar_clientes()

        return redirect("/")

    return render_template("cadastro.html")


# Página dos serviços
@app.route("/servicos")
def servicos_flask():
    return render_template("servicos.html", lista_servicos=PRECOS_SERVICOS)


# Página tipo de veículo
@app.route("/tipo-veiculo")
def tipo_veiculo():
    servico = request.args.get("servico")

    # Se for moto → pula direto
    if servico == "Moto":
        return redirect(f"/agendar?servico=Moto&veiculo=Moto&extra=Nenhum")

    return render_template("tipo-veiculo.html", servico=servico)


# Página de agendamento
@app.route("/agendar")
def agendar():
    servico = request.args.get("servico")
    veiculo = request.args.get("veiculo")
    extra = request.args.get("extra")

    preco_final = PRECOS_SERVICOS.get(servico, 0) + PRECOS_EXTRAS.get(extra, 0)

    return render_template(
        "finalizar.html",
        servico=servico,
        veiculo=veiculo,
        extra_nome=extra,
        extra_valor=PRECOS_EXTRAS.get(extra, 0),
        preco_final=preco_final
    )


# Horários disponíveis
@app.route("/horarios")
def horarios():
    from urllib.parse import unquote
    data_escolhida = request.args.get("data")

    if not data_escolhida:
        return {"horarios": []}

    data_escolhida = unquote(data_escolhida)
    horarios_disponiveis = gerar_horarios_por_dia(data_escolhida)

    return {"horarios": horarios_disponiveis}


# Finalizar agendamento
@app.route("/finalizar", methods=["POST"])
def finalizar():
    data = request.form.get("data")
    hora = request.form.get("hora")

    DIAS_OCUPADOS.add(data)  # salva como ocupado
    agendamento.append({"data": data, "hora": hora})  # salva no JSON

    return render_template("confirmacao.html", data=data, hora=hora)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
