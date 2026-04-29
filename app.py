import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def carregar_chamados():
    try:
        with open("chamados.json", "r") as f:
            return json.load(f)
    except:
        return []

def salvar_chamados(chamados):
    with open("chamados.json", "w") as f:
        json.dump(chamados, f, indent=4)

@app.route("/")
def home():
    chamados = carregar_chamados()
    return render_template("index.html", chamados=chamados)

@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        setor = request.form.get("setor")

        chamados = carregar_chamados()

        chamado = {
            "id": len(chamados) + 1,
            "titulo": titulo,
            "descricao": descricao,
            "setor": setor,
            "status": "aberto"
        }

        chamados.append(chamado)
        salvar_chamados(chamados)

        return redirect("/")

    return render_template("criar.html")

@app.route("/excluir/<int:id>")
def excluir(id):
    chamados = carregar_chamados()
    chamados = [c for c in chamados if c["id"] != id]
    salvar_chamados(chamados)
    return redirect("/")

@app.route("/status/<int:id>")
def mudar_status(id):
    chamados = carregar_chamados()

    for c in chamados:
        if c["status"] == "aberto":
            c["status"] = "em_andamento"
        elif c["status"] == "em_andamento":
            c["status"] = "fechado"
        else:
            c["status"] = "aberto"

    salvar_chamados(chamados)
    return redirect("/")

app.run(debug=True)