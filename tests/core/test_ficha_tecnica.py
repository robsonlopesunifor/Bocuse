import vcr

import pandas as pd

from Bocuse.core.ficha_tecnica import FichaTecnica


class TestFichaTecnica:
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/receita_teste_bolo.yml")
    def test_receita(self):
        receita = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80").receita()
        assert isinstance(receita["equipamentos"],list)
        assert isinstance(receita["ingredientes"],list)
        assert isinstance(receita["informacoes"],dict)
        assert isinstance(receita["preparos"],list)

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_ingredientes.yml")
    def test_ingredientes(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        ingredientes = sheet.ingredientes()
        assert ingredientes[0] == {
            'etapa': 'bolo', 
            'ingredientes': [
                {'nome': 'farinha de trigo', 'quantidade': '400', 'medida': 'gm'},
                {'nome': 'açucar', 'quantidade': '2', 'medida': 'xicara'},
                {'nome': 'bicarbonato de sódio', 'quantidade': '4', 'medida': 'sopa'},
                {'nome': 'fermento químico', 'quantidade': '3', 'medida': 'sobremesa'},
                {'nome': 'sal', 'quantidade': '2', 'medida': 'cha'},
                {'nome': 'baunilha', 'quantidade': '1', 'medida': 'cafe'}
            ]
        }
        assert ingredientes[1] == {
            'etapa': 'cobertura',
            'ingredientes': [
                {'nome': 'creme de leite', 'quantidade': '100', 'medida': 'ml'},
                {'nome': 'chocolate ', 'quantidade': '50', 'medida': 'gm'}
            ]
        }

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_ingredientes.yml")
    def test_informacoes(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        assert sheet.informacoes() == {
            "rendimento": "562",
            "porcao": "100",
            "unidades": "5,62",
            "custo": "0",
        }

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_equipamentos.yml")
    def test_equipamentos(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        assert sheet.equipamentos() == [
            {"nome":"forno", "necessario": True},
            {"nome":"fogão", "necessario": True},
            {"nome":"micro-ondas", "necessario": True},
            {"nome":"termo circulado", "necessario": False},
            {"nome":"geladeira", "necessario": False},
            {"nome":"frise", "necessario": False},
            {"nome":"liquidificador", "necessario": False},
            {"nome":"mixer", "necessario": False},
            {"nome":"processador", "necessario": False},
            {"nome":"batedeira", "necessario": False},
        ]
    
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_bolo_preparo.yml")
    def test_preparo(self):
        sheet = FichaTecnica("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        preparos = sheet.preparos()
        assert preparos == [
            {
                "etapa": "mistura",
                "passos": [
                    {"descricao": "misture os secos", "tipo":""},
                    {"descricao": "misture os liquidos", "tipo":""},
                    {"descricao": "misture os scos e os liquidos", "tipo":"obs"},
                ]
            },
            {
                "etapa": "assar",
                "passos": [
                    {"descricao": "leve ao forno a 180 graus por 1h", "tipo":""},
                ]
            }
        ]

