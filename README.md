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

| Ação | Código |
|------|--------|
| Listagem com resultados | 200 OK |
| Busca por ID encontrado | 200 OK |
| Criação de imóvel | 201 Created |
| Deleção bem-sucedida | 204 No Content |
| Campo obrigatório ausente | 400 Bad Request |
| Recurso não encontrado | 404 Not Found |
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

O deploy na AWS não foi concluído pois o IP da instância EC2 não estava disponível no material enviado pelo professor. O arquivo `.pem` (`progeficaz_25a.pem`) foi recebido, as permissões foram configuradas corretamente e a tentativa de conexão SSH foi realizada, porém sem o IP da instância EC2 não foi possível prosseguir. Todos os demais requisitos foram atendidos, incluindo os critérios de A e A+: códigos HTTP corretos e API no nível 3 de Richardson (HATEOAS).
