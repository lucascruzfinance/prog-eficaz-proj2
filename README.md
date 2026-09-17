# API de Imóveis

API RESTful de imobiliária desenvolvida com Flask e MySQL.

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

## Testes

```bash
pytest test_main.py -v
```

## Códigos HTTP

A API retorna os códigos HTTP corretos para cada ação:

| Ação                     | Código                   |
| -------------------------- | ------------------------- |
| Listagem com resultados    | 200 OK                    |
| Busca por ID encontrado    | 200 OK                    |
| Criação de imóvel       | 201 Created               |
| Deleção bem-sucedida     | 204 No Content            |
| Campo obrigatório ausente | 400 Bad Request           |
| Recurso não encontrado    | 404 Not Found             |
| Erro de conexão com banco | 500 Internal Server Error |

## Nível 3 de Richardson (HATEOAS)

Cada resposta da API inclui `_links` com as ações disponíveis para o recurso, permitindo que o cliente navegue pela API sem conhecer as URLs previamente:

```json
{
  "id": 1,
  "logradouro": "Rua A",
  "_links": {
    "self": "/imoveis/1",
    "imoveis": "/imoveis",
    "atualizar": {"href": "/imoveis/1", "method": "PUT"},
    "deletar": {"href": "/imoveis/1", "method": "DELETE"}
  }
}
```

## Deploy na AWS

API hospedada e acessível em: **http://3.80.44.15:5000/imoveis**

Deploy realizado em instância EC2 Ubuntu 22.04 na AWS, com Gunicorn como servidor WSGI e Nginx como proxy reverso.

Link da AWS:
