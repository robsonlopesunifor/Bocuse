from __future__ import print_function

from fastapi import FastAPI
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from googleapiclient.errors import HttpError

from Bocuse.core.ficha_tecnica import FichaTecnica
from Bocuse.core.google_api import GoogleDrive

app = FastAPI()
folder_root_id = "1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4"


@app.get("/cardapios/")
def cardapios():
    try:
        return GoogleDrive(folder_root_id).listAllSheets()
    except HttpError as error:
        return f"An error occurred: {error}"


@app.get("/receita/{sheed_id}")
def receita(sheed_id: str):
    """
    try:
    """
    status_code = status.HTTP_200_OK
    receita = FichaTecnica(sheed_id).receita()
    response = jsonable_encoder(receita)
    return JSONResponse(content=response, status_code=status_code)
    """
    except Exception :
        status_code = status.HTTP_404_NOT_FOUND
        response = jsonable_encoder({"detail": "FichaTecnica Not found"})
        return JSONResponse(content=response, status_code=status_code)
    """
