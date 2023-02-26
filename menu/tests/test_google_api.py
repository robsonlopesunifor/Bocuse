import pytest
import pandas as pd
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.abspath('../cardapio/'))
from core.google_api import GoogleDrive, GoogleSheet


class TestGoogleDrive:
    def test_listAllSheets(self):
        assert GoogleDrive('1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4').listAllSheets() == [
            {"id":"1lEx-eFWpAhzA2HokOMQIkcVza8Dg6ERq","name":"salgado", 
                "receitas":[{"id":"19TYBsa9Vc6xACUVHz0sNse1AZyK5xsEUtB0R2dBd4BQ","name":"pao"},
                            {"id":"1rfFpqtKIt6jD0mveeOdEzTmBH486GSxG_CrGTf01rAE","name":"pasta"},
                            {"id":"1tKZy2wFduLf-aUMB5dCFiZCFkTfhfsMlvn8XtsWaDxc","name":"pizza"}]},
            {"id":"1XE_4rSji7k9-Xe9Fsy2Xkg9rp26iJ8vC","name":"doces",
                "receitas":[{"id":"1TlI89rhBf2OAJwK_1p_F0ZbnhMF4v7eXy2HqEOT_rTk","name":"pudim"},
                            {"id":"1GChN4mE3tjNtEddbXHvQf2zINUz2tLytCqwVCgdUjeQ","name":"brigadeiro"},
                            {"id":"1CGmEF_YN8BVOn0XfnZ-a_MMrmNTmu28wK58t9hUdols","name":"cookies"}]},
            {"id":"1P_qzVBsmCiWH3iM3T3XhG5yh_d4xQSXq","name":"bebidas",
                "receitas":[{"id":"1v2l5IL_WZbmkX3aVuIWcvhRlbpm149haVyj73OkhQ3A","name":"cafe"}]}
        ]

    def test_searchByReceita(self):
        assert GoogleDrive('1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4').searchByReceita('pizza') == '1tKZy2wFduLf-aUMB5dCFiZCFkTfhfsMlvn8XtsWaDxc'


class TestGoogleSheet:
    def test_dataSheet(self):
        sheet = GoogleSheet('1GChN4mE3tjNtEddbXHvQf2zINUz2tLytCqwVCgdUjeQ')
        df = pd.read_csv('tests/test_bolo.csv')
        assert type(sheet.dataSheet('ingredientes')) == pd.DataFrame

    def test_ingredientes(self):
        sheet = GoogleSheet('')
        df = pd.read_csv('tests/test_bolo.csv')
        assert sheet.ingredientes(df) == [
            {'ingredientes': 'farinha', 'peso': '291', 'preco': '4,5', 'unidade': '1000', 'custo': '1,3095'},
            {'ingredientes': 'agua', 'peso': '300', 'preco': '1', 'unidade': '0', 'custo': '0'},
            {'ingredientes': 'sal', 'peso': '1', 'preco': '2,3', 'unidade': '1000', 'custo': '0,0023'},
            {'ingredientes': 'fermento quimico', 'peso': '21', 'preco': '4,29', 'unidade': '100', 'custo': '0,9009'}
        ]

    def test_informacao(self):
        sheet = GoogleSheet('')
        df = pd.read_csv('tests/test_bolo.csv')
        assert sheet.informacao(df) == {
            'unidades': '6',
            'redimento': '1200',
            'porcao': '200',
            'tempo de preparo': '60',
            'custo compras': '0'
        }
        