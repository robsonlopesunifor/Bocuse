import os
import sys
import vcr
import pytest

import pandas as pd
from Bocuse.core.exceptions import NonExistentPageFault
from Bocuse.core.google_api import GoogleDrive
from Bocuse.core.google_api import GoogleSheet


class TestGoogleDrive:
    @vcr.use_cassette("tests/fixtures/vcr_cassettes/all_sheets.yml")
    def test_listAllSheets(self):
        list_sheets = GoogleDrive("1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4").listAllSheets()
        assert "doces" in (folder["name"] for folder in list_sheets)
        assert "teste_bolo" in (receita["name"] for folder in list_sheets for receita in folder["receitas"])

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/search_receita.yml")
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
        assert isinstance(data, pd.DataFrame)

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/sheet_teste_fails_when_passing_non_existent_page_name.yml")
    def test_dataSheet_fails_when_passing_non_existent_page_name(self):
        sheet = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        with pytest.raises(NonExistentPageFault) as err:
            data = sheet.dataSheet("nome_qualquer")
        assert err.value.STATUS_CODE == 400
        assert err.value.message["message"] == 'O nome do titulo da pagina do fichario não existe.'
        assert err.value.message["error"] =="Unable to parse range: nome_qualquer"

    def test_binder(self):
        sheet = GoogleSheet("1bPHL0LwEQMVSe5CPYX39E2rCpbRpSjo-XJMykK7my80")
        binder = sheet.binder()
        assert "equipamentos" in binder.keys()
        assert isinstance(binder["equipamentos"], pd.DataFrame)
        assert "ingredientes" in binder.keys()
        assert isinstance(binder["ingredientes"], pd.DataFrame)
        assert "preparos" in binder.keys()
        assert isinstance(binder["preparos"], pd.DataFrame)
