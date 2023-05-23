import os
import requests
from pactman import Consumer, Provider, Pact
from Bocuse.configs import settings


PACT_MOCK_HOST="172.17.0.1"
PACT_MOCK_PORT=8000
PACT_DIR=str(settings.PACT_DIR)

pact: Pact = Consumer('Consumer-Lola').has_pact_with(Provider('Provider-Bocuse'), 
        host_name=PACT_MOCK_HOST, port=PACT_MOCK_PORT,pact_dir=PACT_DIR)


class TestBocuse:
    def _test_requisicao(self):
        expected = [{"id":"1lEx-eFWpAhzA2HokOMQIkcVza8Dg6ERq","name":"salgado","receitas":[{"id":"19TYBsa9Vc6xACUVHz0sNse1AZyK5xsEUtB0R2dBd4BQ","name":"teste_pizza"}]},{"id":"1XE_4rSji7k9-Xe9Fsy2Xkg9rp26iJ8vC","name":"doces","receitas":[{"id":"1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80","name":"teste_bolo"}]},{"id":"1P_qzVBsmCiWH3iM3T3XhG5yh_d4xQSXq","name":"bebidas","receitas":[{"id":"1v2l5IL_WZbmkX3aVuIWcvhRlbpm149haVyj73OkhQ3A","name":"teste_cafe"}]}]

        (pact
        .given('UserA exists and is not an administrator')
        .upon_receiving('a request for UserA')
        .with_request('GET', '/cardapios/')
        .will_respond_with(200, body=expected))

        with pact:
            result = requests.get('http://localhost:8000/cardapios/').json()

        assert result == expected