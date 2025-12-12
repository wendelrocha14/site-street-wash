from flask import Flask, render_template, request, redirect
from cadastros import clientes, salvar_clientes
from agenda import gerar_datas_automaticas, gerar_horarios_por_dia, agendamento

app = Flask(__name__)

# Tabela com valores base dos serviços
PRECOS = {
    "Lavagem De Manutenção": 60,
    "Lavagem Detalhada Premium": 70,
    "Moto": 30
}

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

# Serviços
@app.route("/servicos")
def servicos_flask():
    return render_template("servicos.html", lista_servicos=PRECOS)

# Escolher tipo de veículo
@app.route("/tipo-veiculo", methods=["GET", "POST"])
def tipo_veiculo():
    servico = request.args.get("servico")

    if not servico:
        return redirect("/servicos")

    # 🔥 SE O SERVIÇO FOR MOTO → IR DIRETO PARA AGENDAR
    if servico == "Moto":
        return redirect(f"/agendar?servico=Moto&veiculo=Moto&extra=Nenhum")

    # Para os demais serviços (carros), segue a escolha de veículo
    if request.method == "POST":
        veiculo = request.form.get("veiculo")
        extra = request.form.get("extra", "Nenhum")
        return redirect(f"/agendar?servico={servico}&veiculo={veiculo}&extra={extra}")

    return render_template("tipo_veiculo.html", servico=servico)

# Página de agendamento
@app.route("/agendar", methods=["GET"])
def agendar():
    servico = request.args.get("servico")
    veiculo = request.args.get("veiculo")
    extra = request.args.get("extra", "Nenhum")

    # Preços por tipo de carro
    tabela_precos = {
        "Lavagem De Manutenção": {
            "Hatch": 50,
            "Sedan": 55,
            "SUV": 60,
            "Caminhonete": 60
        },
        "Lavagem Detalhada Premium": {
            "Hatch": 65,
            "Sedan": 70,
            "SUV": 75,
            "Caminhonete": 90
        },
        "Moto": {
            "Moto": 30
        }
    }

    preco_servico = tabela_precos.get(servico, {}).get(veiculo, 0)

    extras_precos = {
        "Nenhum": 0,
        "Removedor de Piche": 10,
        "Cera Líquida Premium": 50
    }

    preco_extra = extras_precos.get(extra, 0)

    preco_final = preco_servico + preco_extra

    datas = gerar_datas_automaticas()

    return render_template(
        "agendamentos.html",
        servico=servico,
        veiculo=veiculo,
        extra_nome=extra,
        extra_valor=preco_extra,
        datas=datas,
        preco_final=preco_final
    )

# Horários
@app.route("/horarios")
def horarios():
    from urllib.parse import unquote
    data_escolhida = request.args.get("data")

    if not data_escolhida:
        return {"horarios": []}

    data_escolhida = unquote(data_escolhida)
    horarios_disponiveis = gerar_horarios_por_dia(data_escolhida)

    return {"horarios": horarios_disponiveis}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
