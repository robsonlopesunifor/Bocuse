import vcr

import pandas as pd

from Menu.core.google_api import GoogleSheet
from Menu.core.ficha_tecnica import FichaTecnica


class TestFichaTecnica:
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo.yml")
    def test_fichaTecnica(self):
        ficha_tecnica = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80").fichaTecnica()
        assert isinstance(ficha_tecnica["equipamentos"],dict)
        assert isinstance(ficha_tecnica["ingredientes"],list)
        assert isinstance(ficha_tecnica["informacoes"],dict)
        assert isinstance(ficha_tecnica["preparos"],list)

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_ingredientes.yml")
    def test_ingredientes(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        ingredientes = sheet.ingredientes()
        assert ingredientes[0] == {
            'etapa': 'bolo', 
            'ingredientes': [
                {'ingrediente': 'farinha de trigo', 'valor': '400', 'medida': 'gm'},
                {'ingrediente': 'açucar', 'valor': '2', 'medida': 'xicara'},
                {'ingrediente': 'bicarbonato de sódio', 'valor': '4', 'medida': 'sopa'},
                {'ingrediente': 'fermento químico', 'valor': '3', 'medida': 'sobremesa'},
                {'ingrediente': 'sal', 'valor': '2', 'medida': 'cha'},
                {'ingrediente': 'baunilha', 'valor': '1', 'medida': 'cafe'}
            ]
        }
        assert ingredientes[1] == {
            'etapa': 'cobertura',
            'ingredientes': [
                {'ingrediente': 'creme de leite', 'valor': '100', 'medida': 'ml'},
                {'ingrediente': 'chocolate ', 'valor': '50', 'medida': 'gm'}
            ]
        }

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_ingredientes.yml")
    def test_informacoes(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        assert sheet.informacoes() == {
            "redimento total": "562",
            "porcao": "100",
            "unidades": "5,62",
            "custo": "0",
        }

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_equipamentos.yml")
    def test_equipamentos(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        assert sheet.equipamentos() == {
            "forno": True,
            "fogão": True,
            "micro-ondas": True,
            "termo circulado": False,
            "geladeira": False,
            "frise": False,
            "liquidificador": False,
            "mixer": False,
            "processador": False,
            "batedeira": False,
        }
    
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_preparo.yml")
    def test_preparo(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        etapas = sheet.preparos()
        assert etapas[0] == [
                ('etapa', 'mise en place'),
                ('', 'preaqueça o forno a 180 graus'),
                ('', 'porcione todos os ingredientes')]
        assert etapas[1] == [
                ('etapa', 'mistura dos secos'),
                ('', 'misture os ingredientes secos'),
                ('obs', 'açúcar e um ingrediente liquido')]
        assert etapas[2] == [
                ('etapa','mistura dos molhados'),
                ('', 'misture os ingredientes molhados'),
                ('', 'derreta a manteiga e use sua tigela para misturar os ingredientes')]
        assert etapas[3] == [
                ('etapa','mistura dos secos e dos molhados'),
                ('', 'misture com calma para não ativar o glúten'),
                ('', 'procure misturar o mínimo possível')]
        assert etapas[4] == [
                ('etapa','forno'),
                ('', 'unte a forma com manteiga ou um deformante'),
                ('', 'coloque a massa na forma')]
        assert etapas[5] == [
                ('etapa','cobertura'),
                ('', 'derreta o chocolate com o creme de leite no micro-ondas')]
