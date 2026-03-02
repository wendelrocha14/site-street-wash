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
        return redirect(f"/agendar?servico={servico}&veiculo={veiculo}")
    return render_template("tipo_veiculo.html", servico=servico)


# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
# 4. TELA FINAL (VALOR TOTAL)
# ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬


@app.route("/agendar")
def agendar():
    servico_raw = request.args.get("servico")
    veiculo = request.args.get("veiculo")

    if not servico_raw or not veiculo:
        return "Serviço ou veículo não selecionado"

    servico = normalizar_servico(servico_raw)

    # Buscar preço correto da tabela principal
    preco_base = PRECOS_VEICULOS.get(servico, {}).get(veiculo)

    if preco_base is None:
        return "Preço não encontrado"

    datas = [
        "26/02/2026",
        "27/02/2026",
        "28/02/2026",
        "01/03/2026"
    ]

    return render_template(
        "agendamentos.html",
        servico=servico,
        veiculo=veiculo,
        preco_base=preco_base,
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