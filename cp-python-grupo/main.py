
from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from eventotech.models.evento import Evento
from dao.evento_dao import EventoDAO


app = Flask(
    __name__,
    template_folder="eventotech/templates",
    static_folder="eventotech/static"
)

app.secret_key = "chave-de-desenvolvimento"

dao = EventoDAO()


CAMPOS = (
    "id_evento", "nome_evento", "categoria", "data_evento",
    "local_evento", "capacidade", "valor_ingresso",
    "responsavel", "status", "data_cadastro"
)


def transformar_evento(registro):
    if registro is None:
        return None

    if isinstance(registro, dict):
        return registro

    return dict(zip(CAMPOS, registro))


def ler_formulario(id_evento=None):
    try:
        identificador = (
            id_evento
            if id_evento is not None
            else int(request.form["id_evento"])
        )

        nome = request.form.get("nome_evento", "").strip()
        categoria = request.form.get("categoria", "").strip()
        data = datetime.strptime(
            request.form["data_evento"], "%Y-%m-%d"
        )
        local = request.form.get("local_evento", "").strip()
        capacidade = int(request.form["capacidade"])
        valor = Decimal(
            request.form.get("valor_ingresso") or "0"
        )
        responsavel = request.form.get("responsavel", "").strip()
        status = (
            request.form.get("status", "ATIVO").strip()
            or "ATIVO"
        )

    except (KeyError, ValueError, InvalidOperation) as erro:
        raise ValueError(
            "Confira os campos numéricos e a data do evento."
        ) from erro

    if identificador <= 0 or capacidade <= 0 or not valor.is_finite() or valor < 0:
        raise ValueError(
            "ID e capacidade devem ser positivos e o valor válido."
        )

    if not all((nome, categoria, local, responsavel)):
        raise ValueError(
            "Nome, categoria, local e responsável são obrigatórios."
        )

    return Evento(
        identificador,
        nome,
        categoria,
        data,
        local,
        capacidade,
        valor,
        responsavel,
        status
    )


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/eventos")
def listar():
    registros = dao.listar_eventos()

    if registros is False:
        return "Não foi possível consultar o banco.", 503

    eventos = [
        transformar_evento(r)
        for r in (registros or [])
    ]

    return render_template("eventos.html", eventos=eventos)


@app.route("/eventos/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        try:
            evento = ler_formulario()
            resultado = dao.cadastrar_evento(evento)

            if resultado is True:
                flash("Evento cadastrado com sucesso!")
                return redirect(url_for("listar"))

            flash("Não foi possível cadastrar o evento.")

        except ValueError as erro:
            flash(str(erro))

    return render_template("cadastrar.html")


@app.route("/eventos/<int:id>")
def detalhes(id):
    registro = dao.buscar_id_evento(id)

    if registro is False:
        return "Banco de dados indisponível.", 503

    if registro is None:
        return "Evento não encontrado.", 404

    evento = transformar_evento(registro)

    return render_template(
        "detalhes.html",
        evento=evento
    )


@app.route("/eventos/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    registro = dao.buscar_id_evento(id)

    if registro is False:
        return "Banco de dados indisponível.", 503

    if registro is None:
        return "Evento não encontrado.", 404

    if request.method == "POST":
        try:
            evento = ler_formulario(id)
            resultado = dao.editar_evento(evento)

            if resultado is True:
                flash("Evento atualizado com sucesso!")
                return redirect(url_for("listar"))

            if resultado is None:
                return "Evento não encontrado.", 404

            flash("Erro ao atualizar o evento.")

        except ValueError as erro:
            flash(str(erro))

    evento = transformar_evento(registro)

    return render_template(
        "editar.html",
        evento=evento
    )


@app.route("/eventos/excluir/<int:id>", methods=["POST"])
def excluir(id):
    resultado = dao.excluir_evento(id)

    if resultado is True:
        flash("Evento excluído com sucesso!")

    elif resultado is None:
        flash("Evento não encontrado.")

    else:
        flash("Erro ao excluir o evento.")

    return redirect(url_for("listar"))


@app.route("/api/eventos")
def api_eventos():
    registros = dao.listar_eventos()

    if registros is False:
        return jsonify({"erro": "Banco indisponível"}), 503

    eventos = [
        transformar_evento(r)
        for r in (registros or [])
    ]

    return jsonify(eventos)


if __name__ == "__main__":
    app.run(debug=True)
