import os.path
import pandas as pd
from tabulate import tabulate
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

folder_menu_id = '1WbimQ3P31IOYWv_zsCdnGaxsMF6be5J4'

class GoogleApi:

    def credencial(self):
        creds = None
        if os.path.exists('core/token.json'):
            creds = Credentials.from_authorized_user_file('core/token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'core/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('core/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds


class GoogleDrive(GoogleApi):
    def __init__(self, folder_id:str):
        self.service = build('drive', 'v3', credentials=self.credencial())
        self.folder_id = folder_id

    def listAllSheets(self):
        cardapios = self.folderList()
        for cardapio in cardapios:
            planilhas = self.sheetsList(cardapio['id'])
            cardapio['receitas'] = planilhas
        return cardapios

    def folderList(self):
        results = self.service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and '{0}' in parents".format(self.folder_id),
            pageSize=20, fields="nextPageToken, files(id, name)").execute()
        return results.get('files', [])

    def sheetsList(self, folder_id):
        results = self.service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet' and '{0}' in parents".format(folder_id),
            fields="nextPageToken, files(id, name)").execute()
        return results.get('files', [])

    def searchByReceita(self, nome_receita:str):
        menu = self.listAllSheets()
        for cardapio in menu:
            for receita in cardapio['receitas']:
                if receita['name'] == nome_receita: 
                    return receita['id']
        return None

class GoogleSheet(GoogleApi):
    def __init__(self, sheet_id:str):
        self.service = build('sheets', 'v4', credentials=self.credencial())
        self.sheet_id = sheet_id
        self.ficha_tecnica = {}

    def carregar():
        data_frame = self.dataSheet('ingredientes!A:E')
        self.ficha_tecnica['ingredientes'] = self.ingredientes(data_frame)

    def dataSheet(self, range:str):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id,range=range).execute()
        data_frame = pd.DataFrame(result.get('values', []))
        data_frame.to_csv('tests/test_bolo.csv')
        return data_frame

    def ingredientes(self, data_frame):
        novas_chaves = data_frame.iloc[3:4,1:].to_dict('records')
        novo_df = data_frame.iloc[4:,1:].rename(columns=novas_chaves[0])
        ingredientes = novo_df.to_dict('records')
        return ingredientes

    def informacao(self, data_frame):
        novas_chaves = data_frame.iloc[1:2,1:].to_dict('records')
        novo_df = data_frame.iloc[2:3,1:].rename(columns=novas_chaves[0])
        ingredientes = novo_df.to_dict('records')[0]
        return ingredientes