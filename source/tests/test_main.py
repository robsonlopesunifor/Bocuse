import os
import sys

from fastapi.testclient import TestClient
from main import app

sys.path.insert(0, os.path.abspath("../source/"))


client = TestClient(app)


def test_cardapios():
    response = client.get("/cardapios/")
    list_sheets = response.json()
    assert response.status_code == 200
    assert "doces" in (folder["name"] for folder in list_sheets)
    assert "teste_bolo" in (receita["name"] for folder in list_sheets for receita in folder["receitas"])


def test_receita():
    response = client.get("/receita/teste_cafe")
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
