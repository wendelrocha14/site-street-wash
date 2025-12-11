import json
import os

ARQ_CLIENTES = "clientes.json"

def carregar_clientes():
    if os.path.exists(ARQ_CLIENTES):
        with open(ARQ_CLIENTES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

clientes = carregar_clientes()

def salvar_clientes():
    with open(ARQ_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)
