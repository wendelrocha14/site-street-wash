from flask import Flask, render_template, request, redirect
from cadastros import clientes, salvar_clientes
from agenda import gerar_datas_automaticas, gerar_horarios_por_dia

app = Flask(__name__)

# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# 1. TABELAS DE PREÇO
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

PRECOS_SERVICO = {
    "lavagem-manutencao": 50,
    "lavagem-premium": 70,
    "moto": 30
}

PRECOS_VEICULOS = {
    "lavagem-manutencao": {
        "Hatch": 50,
        "Sedan": 55,
        "SUV": 60,
        "Caminhonete": 60
    },
    "lavagem-premium": {
        "Hatch": 65,
        "Sedan": 70,
        "SUV": 75,
        "Caminhonete": 90
    },
    "moto": {
        "Moto": 30
    }
}

PRECOS_EXTRAS = {
    "Nenhum": 0,
    "Removedor de Piche": 10,
    "Cera Líquida Premium": 50
}

# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# FUNÇÃO DE NORMALIZAÇÃO
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

def normalizar_servico(nome):
    nome = nome.lower().strip()

    if "manutenção" in nome or "manutencao" in nome:
        return "lavagem-manutencao"

    if "premium" in nome:
        return "lavagem-premium"

    if "moto" in nome:
        return "moto"

    return nome


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# 2. ROTAS PRINCIPAIS
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        clientes.append({"nome": nome, "telefone": telefone})
        salvar_clientes()
        return redirect("/")
    return render_template("cadastro.html")


@app.route("/servicos")
def servicos_flask():
    return render_template("servicos.html")


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# 3. TIPO DE VEÍCULO
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

@app.route("/tipo-veiculo", methods=["GET", "POST"])
def tipo_veiculo():
    servico_raw = request.args.get("servico", "")
    servico = normalizar_servico(servico_raw)

    # Se o serviço for moto → pula direto para a tela final
    if servico == "moto":
        return redirect(f"/agendar?servico=moto&veiculo=Moto&extra=Nenhum")

    # Se usuário clicou em continuar
    if request.method == "POST":
        veiculo = request.form.get("veiculo")
        extra = request.form.get("extra", "Nenhum")
        return redirect(f"/agendar?servico={servico}&veiculo={veiculo}&extra={extra}")

    return render_template("tipo_veiculo.html", servico=servico)


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# 4. TELA FINAL (VALOR TOTAL)
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

@app.route("/agendar", methods=["GET"])
def agendar():

    servico_raw = request.args.get("servico", "")
    servico = normalizar_servico(servico_raw)

    veiculo = request.args.get("veiculo", "")
    extra = request.args.get("extra", "Nenhum")

    # Preço base (conforme serviço e veículo)
    preco_servico = PRECOS_VEICULOS.get(servico, {}).get(veiculo, 0)

    # Preço do extra
    preco_extra = PRECOS_EXTRAS.get(extra, 0)

    # Soma total
    preco_total = preco_servico + preco_extra

    # Datas disponíveis
    datas = gerar_datas_automaticas()

    return render_template(
        "agendamentos.html",
        servico=servico,
        veiculo=veiculo,
        extra_nome=extra,
        extra_valor=preco_extra,
        preco_final=preco_total,
        datas=datas
    )


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# 5. HORÁRIOS
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

@app.route("/horarios")
def horarios():
    from urllib.parse import unquote

    data_escolhida = request.args.get("data", "")
    if not data_escolhida:
        return {"horarios": []}

    data_escolhida = unquote(data_escolhida)
    horarios_disponiveis = gerar_horarios_por_dia(data_escolhida)

    return {"horarios": horarios_disponiveis}


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# EXECUTAR LOCAL
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)