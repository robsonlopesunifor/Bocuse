import os.path

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError

from Bocuse.core.exceptions import NonExistentPageFault
from Bocuse.core.utils import returnMessageError

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleApi:
    def credencial(self):
        creds = None
        if os.path.exists("Bocuse/core/token.json"):
            creds = Credentials.from_authorized_user_file("Bocuse/core/token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("Bocuse/core/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("Bocuse/core/token.json", "w") as token:
                token.write(creds.to_json())
        return creds


class GoogleDrive(GoogleApi):
    def __init__(self, folder_id: str):
        self.service = build("drive", "v3", credentials=self.credencial())
        self.folder_id = folder_id

    def searchFichaTecnica(self, nome_receita: str):
        menu = self.listAllSheets()
        for cardapio in menu:
            for receita in cardapio["receitas"]:
                if receita["name"] == nome_receita:
                    return receita["id"]
        return None

    def listAllSheets(self):
        cardapios = self.folderList()
        for cardapio in cardapios:
            planilhas = self.sheetsList(cardapio["id"])
            cardapio["receitas"] = planilhas
        return cardapios

    def folderList(self):
        results = (
            self.service.files()
            .list(
                q="mimeType='application/vnd.google-apps.folder' and '{0}' in parents".format(self.folder_id),
                pageSize=20,
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        return results.get("files", [])

    def sheetsList(self, folder_id):
        results = (
            self.service.files()
            .list(
                q="mimeType='application/vnd.google-apps.spreadsheet' and '{0}' in parents".format(folder_id),
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        return results.get("files", [])


class GoogleSheet(GoogleApi):
    def __init__(self, sheet_id: str):
        self.service = build("sheets", "v4", credentials=self.credencial())
        self.sheet_id = sheet_id

    def dataSheet(self, range: str):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id, range=range).execute()
            return pd.DataFrame(result.get("values", []))
        except GoogleHttpError as error:
            message_erro = returnMessageError(error.content)
            raise NonExistentPageFault(message_erro)

    def binder(self):
        sheet = self.service.spreadsheets()
        sheets = sheet.get(spreadsheetId=self.sheet_id).execute()
        binder = {}
        for sheet in sheets["sheets"]:
            title = sheet["properties"]["title"]
            binder[title] = self.dataSheet(title)
        return binder
