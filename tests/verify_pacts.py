import requests
from pactman.verifier.verify import ProviderStateMissing

def provider_state(name, **params):
    if name == "UserA exists and is not an administrator":
        print("===========================================")
        print(name, params)
    else:
        raise ProviderStateMissing(name)

def test_pacts(pact_verifier):
    pact_verifier.verify(provider_setup=provider_state, provider_url="http://localhost:8000")