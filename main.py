import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

COLUNAS = ["id", "logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"]


def conectar_banco():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("DB_SSL_CA"),
        port=int(os.getenv("DB_PORT"))
    )
    return conn


def row_para_dict(row):
    return dict(zip(COLUNAS, row))


def adicionar_links(imovel):
    imovel_id = imovel["id"]
    imovel["_links"] = {
        "self": f"/imoveis/{imovel_id}",
        "imoveis": "/imoveis",
        "atualizar": {"href": f"/imoveis/{imovel_id}", "method": "PUT"},
        "deletar": {"href": f"/imoveis/{imovel_id}", "method": "DELETE"}
    }
    return imovel


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "_links": {"imoveis": "/imoveis"}}), 200


@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")

    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500

    cursor = conn.cursor()

    if tipo:
        cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    elif cidade:
        cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    else:
        cursor.execute("SELECT * FROM imoveis")

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({"erro": "Nenhum imóvel encontrado"}), 404

    imoveis = [adicionar_links(row_para_dict(row)) for row in rows]
    return jsonify({
        "imoveis": imoveis,
        "_links": {"self": "/imoveis"}
    }), 200


@app.route("/imoveis/<int:id>", methods=["GET"])
def buscar_imovel(id):
    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    imovel = adicionar_links(row_para_dict(row))
    return jsonify(imovel), 200


@app.route("/imoveis", methods=["POST"])
def criar_imovel():
    dados = request.get_json()

    if not dados or "logradouro" not in dados or "cidade" not in dados:
        return jsonify({"erro": "Campos obrigatórios: logradouro e cidade"}), 400

    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500

    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            dados.get("logradouro"),
            dados.get("tipo_logradouro"),
            dados.get("bairro"),
            dados.get("cidade"),
            dados.get("cep"),
            dados.get("tipo"),
            dados.get("valor"),
            dados.get("data_aquisicao")
        )
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": novo_id,
        "mensagem": "Imóvel criado com sucesso",
        "_links": {
            "self": f"/imoveis/{novo_id}",
            "imoveis": "/imoveis"
        }
    }), 201


@app.route("/imoveis/<int:id>", methods=["PUT"])
def atualizar_imovel(id):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos = []
    valores = []
    for campo in ["logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"]:
        if campo in dados:
            campos.append(f"{campo} = %s")
            valores.append(dados[campo])

    if not campos:
        return jsonify({"erro": "Nenhum campo válido para atualizar"}), 400

    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500

    valores.append(id)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE imoveis SET {', '.join(campos)} WHERE id = %s", valores)
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    conn.close()
    return jsonify({
        "mensagem": "Imóvel atualizado com sucesso",
        "_links": {
            "self": f"/imoveis/{id}",
            "imoveis": "/imoveis"
        }
    }), 200


@app.route("/imoveis/<int:id>", methods=["DELETE"])
def deletar_imovel(id):
    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar ao banco de dados"}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    conn.close()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
