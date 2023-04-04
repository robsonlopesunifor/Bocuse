from __future__ import print_function

from fastapi import FastAPI
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from googleapiclient.errors import HttpError

from Menu.core.ficha_tecnica import FichaTecnica
from Menu.core.google_api import GoogleDrive

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
        status_code = status.HTTP_200_OK
        sheed_id = GoogleDrive(folder_root_id).searchFichaTecnica(ficha_tecnica_title)
        ficha_tecnica = FichaTecnica(sheed_id).fichaTecnica()
        response = jsonable_encoder(ficha_tecnica)
        return JSONResponse(content=response, status_code=status_code)
    except Exception:
        status_code = status.HTTP_404_NOT_FOUND
        response = jsonable_encoder({"detail": "Ficha Tecnica Not found"})
        return JSONResponse(content=response, status_code=status_code)
