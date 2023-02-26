from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.abspath('../cardapio/'))
from main import app

client = TestClient(app)


def test_cardapios():
    response = client.get("/cardapios/")
    assert response.status_code == 200
    assert response.json() == [
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

def test_receita():
    response = client.get("/receita/bolo")
    assert response.status_code == 200
    assert response.json() == {
            'porsao':8,
            'gasto':80.00,
            'custo':10.10,
            'ingredientes':[
                {'nome':'farinha','gramas':'400'},
                {'nome':'aguq','gramas':'300'},
                {'nome':'sal','gramas':'200'}
            ]
        }