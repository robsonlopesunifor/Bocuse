from __future__ import print_function

from typing import Union
from fastapi import FastAPI
from googleapiclient.errors import HttpError
from core.google_api import GoogleDrive, GoogleSheet


app = FastAPI()
folder_root_id = '1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4'

@app.get("/cardapios/")
def cardapios():
    try:
        return GoogleDrive(folder_root_id).listAllSheets()
    except HttpError as error:
        return f'An error occurred: {error}'

@app.get("/receita/{nome_receita}")
def receita(nome_receita: str):
    try:
        sheed_id = GoogleDrive(folder_root_id).searchByReceita(nome_receita)
        lista_ingredientes = GoogleSheet(sheed_id).dataSheet('Pagina1!A1:B3')
        lista_ingredientes = GoogleSheet(sheed_id).dataSheet('Pagina1!A1:B3')
    except HttpError as error:
        return f'An error occurred: {error}'
