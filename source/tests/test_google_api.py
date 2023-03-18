import os
import sys

import pandas as pd

from core.google_api import GoogleDrive
from core.google_api import GoogleSheet

sys.path.insert(0, os.path.abspath("../source/"))


class TestGoogleDrive:
    def test_listAllSheets(self):
        list_sheets = GoogleDrive("1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4").listAllSheets()
        assert "doces" in (folder["name"] for folder in list_sheets)
        assert "teste_bolo" in (receita["name"] for folder in list_sheets for receita in folder["receitas"])

    def test_searchByReceita(self):
        assert (
            GoogleDrive("1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4").searchByReceita("teste_bolo")
            == "1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80"
        )


class TestGoogleSheet:
    def test_dataSheet(self):
        sheet = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        df = pd.DataFrame(pd.read_csv("source/tests/test_bolo.csv", index_col=0).values)
        data = sheet.dataSheet("ingredientes")
        assert (data.values == df.values).all()

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

    def test_ingredientes(self):
        sheet = GoogleSheet("")
        df = pd.DataFrame(pd.read_csv("source/tests/test_bolo.csv", index_col=0).values)
        assert sheet.ingredientes(df) == [
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

    def test_informacoes(self):
        sheet = GoogleSheet("")
        df = pd.DataFrame(pd.read_csv("source/tests/test_bolo.csv", index_col=0).values)
        # import pdb; pdb.set_trace()
        assert sheet.informacoes(df) == {
            "unidades": "6",
            "redimento": "1200",
            "porcao": "200",
            "tempo de preparo": "60",
            "custo compras": "0",
        }
        assert 1 == 1
