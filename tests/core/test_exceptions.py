import pytest
from Bocuse.core.exceptions import NonExistentPageFault

def test_NonExistentPageFault():
    error = "mensagem de erro originl"
    with pytest.raises(NonExistentPageFault) as err:
        raise NonExistentPageFault(error)
    assert err.value.STATUS_CODE == 400
    assert err.value.message["message"] == 'O nome do titulo da pagina do fichario não existe.'
    assert err.value.message["error"] == error