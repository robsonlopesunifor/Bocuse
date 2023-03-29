import os
import sys
import vcr

from fastapi.testclient import TestClient
from Menu.main import app


client = TestClient(app)


@vcr.use_cassette("tests/fixtures/vcr_cassettes/cardapio.yml")
def test_cardapios():
    response = client.get("/cardapios/")
    list_sheets = response.json()
    assert response.status_code == 200
    assert "doces" in (folder["name"] for folder in list_sheets)
    assert "teste_bolo" in (receita["name"] for folder in list_sheets for receita in folder["receitas"])


@vcr.use_cassette("tests/fixtures/vcr_cassettes/ficha_tecnica_teste_bolo.yml")
def test_ficha_tecnica():
    response = client.get("/ficha_tecnica/teste_bolo")
    ficha_tecnica = response.json()
    assert response.status_code == 200
    assert "informacoes" in list(ficha_tecnica.keys())
    assert "ingredientes" in list(ficha_tecnica.keys())
    assert "unidades" in list(ficha_tecnica["informacoes"].keys())
    assert "redimento" in list(ficha_tecnica["informacoes"].keys())
    assert "porcao" in list(ficha_tecnica["informacoes"].keys())
    assert "tempo de preparo" in list(ficha_tecnica["informacoes"].keys())
    assert "custo compras" in list(ficha_tecnica["informacoes"].keys())
    assert "ingredientes" in list(ficha_tecnica["ingredientes"][0].keys())
    assert "peso" in list(ficha_tecnica["ingredientes"][0].keys())
    assert "preco" in list(ficha_tecnica["ingredientes"][0].keys())
    assert "unidade" in list(ficha_tecnica["ingredientes"][0].keys())
    assert "custo" in list(ficha_tecnica["ingredientes"][0].keys())
