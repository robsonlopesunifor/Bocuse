import os
import sys
import vcr

import pandas as pd

from Menu.core.google_api import GoogleDrive
from Menu.core.google_api import GoogleSheet


class TestGoogleDrive:
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/all_sheets.yml")
    def test_listAllSheets(self):
        list_sheets = GoogleDrive("1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4").listAllSheets()
        assert "doces" in (folder["name"] for folder in list_sheets)
        assert "teste_bolo" in (receita["name"] for folder in list_sheets for receita in folder["receitas"])

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/search_ficha_tecnica.yml")
    def test_searchFichaTecnica(self):
        assert (
            GoogleDrive("1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4").searchFichaTecnica("teste_bolo")
            == "1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80"
        )


class TestGoogleSheet:
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo.yml")
    def test_dataSheet(self):
        sheet = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        data = sheet.dataSheet("ingredientes")
        assert data.values[:1][0].tolist() == ["unidades", "redimento", "porcao", "tempo de preparo", "custo compras"]

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo.yml")
    def test_fichaTecnica(self):
        ficha_tecnica = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80").fichaTecnica()
        assert ficha_tecnica == {
            "informacoes": {
                "unidades": "6",
                "redimento": "1200",
                "porcao": "200",
                "tempo de preparo": "60",
                "custo compras": "0",
            },
            "ingredientes": [
                {
                    "ingredientes": "farinha",
                    "peso": "291",
                    "preco": "4,5",
                    "unidade": "1000",
                    "custo": "1,3095",
                },
                {
                    "ingredientes": "agua",
                    "peso": "300",
                    "preco": "1",
                    "unidade": "0",
                    "custo": "0",
                },
                {
                    "ingredientes": "sal",
                    "peso": "1",
                    "preco": "2,3",
                    "unidade": "1000",
                    "custo": "0,0023",
                },
                {
                    "ingredientes": "fermento quimico",
                    "peso": "21",
                    "preco": "4,29",
                    "unidade": "100",
                    "custo": "0,9009",
                },
            ],
        }

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo.yml")
    def test_ingredientes(self):
        sheet = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        data = sheet.dataSheet("ingredientes")
        assert sheet.ingredientes(data) == [
            {
                "ingredientes": "farinha",
                "peso": "291",
                "preco": "4,5",
                "unidade": "1000",
                "custo": "1,3095",
            },
            {
                "ingredientes": "agua",
                "peso": "300",
                "preco": "1",
                "unidade": "0",
                "custo": "0",
            },
            {
                "ingredientes": "sal",
                "peso": "1",
                "preco": "2,3",
                "unidade": "1000",
                "custo": "0,0023",
            },
            {
                "ingredientes": "fermento quimico",
                "peso": "21",
                "preco": "4,29",
                "unidade": "100",
                "custo": "0,9009",
            },
        ]

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo.yml")
    def test_informacoes(self):
        sheet = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        data = sheet.dataSheet("ingredientes")
        assert sheet.informacoes(data) == {
            "unidades": "6",
            "redimento": "1200",
            "porcao": "200",
            "tempo de preparo": "60",
            "custo compras": "0",
        }
