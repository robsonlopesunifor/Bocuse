import os
import sys
import vcr

from fastapi.testclient import TestClient
from Bocuse.main import app


client = TestClient(app)


@vcr.use_cassette("tests/fixtures/vcr_cassettes/cardapio.yml")
def test_cardapios():
    response = client.get("/cardapios/")
    list_sheets = response.json()
    assert response.status_code == 200
    assert "doces" in (folder["name"] for folder in list_sheets)
    assert "teste_bolo" in (receita["name"] for folder in list_sheets for receita in folder["receitas"])


@vcr.use_cassette("tests/fixtures/vcr_cassettes/receita_teste_bolo.yml")
def test_get_receita():
    response = client.get("/receita/1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
    assert response.status_code == 200
    
@vcr.use_cassette("tests/fixtures/vcr_cassettes/receita_teste_bolo_404.yml")
def test_get_erro_receita():
    response = client.get("/receita/erro")
    assert response.status_code == 404
