import pytest
from unittest.mock import patch, MagicMock
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ===== GET /imoveis =====

@patch("main.conectar_banco")
def test_listar_todos_imoveis_retorna_200(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Rua A", "Rua", "Centro", "São Paulo", "01310-100", "apartamento", 500000.0, "2020-01-01"),
    ]
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis")

    # Then
    assert response.status_code == 200
    data = response.get_json()
    assert "imoveis" in data
    assert len(data["imoveis"]) == 1


@patch("main.conectar_banco")
def test_listar_imoveis_sem_registros_retorna_404(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis")

    # Then
    assert response.status_code == 404


@patch("main.conectar_banco")
def test_listar_imoveis_erro_banco_retorna_500(mock_conectar, client):
    # Given
    mock_conectar.return_value = None

    # When
    response = client.get("/imoveis")

    # Then
    assert response.status_code == 500


# ===== GET /imoveis/<id> =====

@patch("main.conectar_banco")
def test_buscar_imovel_por_id_retorna_200(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, "Rua A", "Rua", "Centro", "São Paulo", "01310-100", "apartamento", 500000.0, "2020-01-01"
    )
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis/1")

    # Then
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["cidade"] == "São Paulo"


@patch("main.conectar_banco")
def test_buscar_imovel_inexistente_retorna_404(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis/9999")

    # Then
    assert response.status_code == 404


# ===== POST /imoveis =====

@patch("main.conectar_banco")
def test_criar_imovel_retorna_201(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 101
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar.return_value = mock_conn

    novo = {
        "logradouro": "Av. Paulista",
        "tipo_logradouro": "Avenida",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "cep": "01310-100",
        "tipo": "apartamento",
        "valor": 750000.0,
        "data_aquisicao": "2022-06-15"
    }

    # When
    response = client.post("/imoveis", json=novo)

    # Then
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["id"] == 101


@patch("main.conectar_banco")
def test_criar_imovel_sem_cidade_retorna_400(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_conectar.return_value = mock_conn

    incompleto = {"logradouro": "Rua B"}

    # When
    response = client.post("/imoveis", json=incompleto)

    # Then
    assert response.status_code == 400


@patch("main.conectar_banco")
def test_criar_imovel_sem_logradouro_retorna_400(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_conectar.return_value = mock_conn

    incompleto = {"cidade": "Campinas"}

    # When
    response = client.post("/imoveis", json=incompleto)

    # Then
    assert response.status_code == 400


# ===== PUT /imoveis/<id> =====

@patch("main.conectar_banco")
def test_atualizar_imovel_retorna_200(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar.return_value = mock_conn

    dados = {"valor": 450000.0, "tipo": "casa"}

    # When
    response = client.put("/imoveis/1", json=dados)

    # Then
    assert response.status_code == 200


@patch("main.conectar_banco")
def test_atualizar_imovel_inexistente_retorna_404(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar.return_value = mock_conn

    dados = {"valor": 450000.0}

    # When
    response = client.put("/imoveis/9999", json=dados)

    # Then
    assert response.status_code == 404


# ===== DELETE /imoveis/<id> =====

@patch("main.conectar_banco")
def test_deletar_imovel_retorna_204(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar.return_value = mock_conn

    # When
    response = client.delete("/imoveis/1")

    # Then
    assert response.status_code == 204


@patch("main.conectar_banco")
def test_deletar_imovel_inexistente_retorna_404(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar.return_value = mock_conn

    # When
    response = client.delete("/imoveis/9999")

    # Then
    assert response.status_code == 404


# ===== GET /imoveis?tipo=<tipo> =====

@patch("main.conectar_banco")
def test_buscar_por_tipo_retorna_200(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (3, "Rua C", "Rua", "Jardins", "São Paulo", "01452-000", "casa", 1200000.0, "2021-07-20"),
    ]
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis?tipo=casa")

    # Then
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["imoveis"]) == 1
    assert data["imoveis"][0]["tipo"] == "casa"


@patch("main.conectar_banco")
def test_buscar_por_tipo_inexistente_retorna_404(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis?tipo=castelo")

    # Then
    assert response.status_code == 404


# ===== GET /imoveis?cidade=<cidade> =====

@patch("main.conectar_banco")
def test_buscar_por_cidade_retorna_200(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (2, "Av. Brasil", "Avenida", "Centro", "Rio de Janeiro", "20040-020", "casa", 800000.0, "2019-03-15"),
    ]
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis?cidade=Rio de Janeiro")

    # Then
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["imoveis"]) == 1
    assert data["imoveis"][0]["cidade"] == "Rio de Janeiro"


@patch("main.conectar_banco")
def test_buscar_por_cidade_inexistente_retorna_404(mock_conectar, client):
    # Given
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_conectar.return_value = mock_conn

    # When
    response = client.get("/imoveis?cidade=Narnia")

    # Then
    assert response.status_code == 404
