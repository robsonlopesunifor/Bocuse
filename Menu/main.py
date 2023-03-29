from __future__ import print_function

from fastapi import FastAPI

from googleapiclient.errors import HttpError

from Menu.core.google_api import GoogleDrive
from Menu.core.google_api import GoogleSheet

app = FastAPI()
folder_root_id = "1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4"


@app.get("/cardapios/")
def cardapios():
    try:
        return GoogleDrive(folder_root_id).listAllSheets()
    except HttpError as error:
        return f"An error occurred: {error}"


@app.get("/ficha_tecnica/{ficha_tecnica_title}")
def receita(ficha_tecnica_title: str):
    try:
        sheed_id = GoogleDrive(folder_root_id).searchFichaTecnica(ficha_tecnica_title)
        return GoogleSheet(sheed_id).fichaTecnica()
    except HttpError as error:
        return f"An error occurred: {error}"
