import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import timedelta, datetime
import pandas as pd
import streamlit as st


json = {
    "type": "service_account",
    "project_id": st.secrets['project_id'],
    "private_key_id": st.secrets['KEY'],
    "private_key": st.secrets['private_key'],
    "client_email": st.secrets['client_email'],
    "client_id": st.secrets['client_id'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/case-693%40digital-layout-402513.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json, scope)

# Cria um serviço da API do Google Drive
drive_service = build('drive', 'v3', credentials=credentials)

client = gs.authorize(credentials)

sheet = client.open_by_key(st.secrets['sheet'])

base = sheet.worksheet('Base')

base_len = sheet.worksheet('Base_Len')
hist_len = sheet.worksheet('Histórico_Len')
base_cad = client.open_by_key(st.secrets['base_cad']).worksheet('CAD')

def solicitacao(s):
    pedidos = base.get_values('B:B')
    l = []
    for p in pedidos:
        l.append(p[0])

    if str(s.pedido) in l:
        return 'Pedido já cadastrado.'
    
    last_row = 'a' + str(len(pedidos) + 1)    
    now = datetime.now() - timedelta(hours=3)
    now = now.strftime('%d/%m/%Y %H:%M:%S')

    base.update([[now,s.filial, s.pedido, s.pedido_novo, s.item, s.descricao, s.motivo, s.obs, s.destino, s.regiao, s.arquivo, 'Solicitado Filial']], last_row,value_input_option='USER_ENTERED')
    return 'Pedido Registrado'



def upload_arquivo(arquivo, nome):
    nome = str(nome)
    tipo = arquivo.type
    tipo = tipo.split('/')[1]
    
    with open(nome + f".{tipo}", "wb") as f:
        f.write(arquivo.read())

    file_metadata = {'name': f'{nome}.{tipo}'}
    media = MediaFileUpload(nome + f".{tipo}", mimetype=arquivo.type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

  
    drive_service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    
    file_id = file.get('id')
    file_link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing' #link de compartilhamento

    return file_link


def consultar_pedidos(pedido=None, filial=0):
    df = pd.DataFrame(base.get_values('a2:l'))
    df = df[[0,1,2,3,8,11]]
    df.columns = ['Registro', 'Filial', 'Pedido', 'Pedido Novo', 'Destino', 'Status']
    df['Pedido'] =  df['Pedido'].astype(str)
    df = df.loc[df['Filial'] == str(filial)]
    if pedido:
        return df.loc[df['Pedido'] == str(pedido)]
    else:
        return df
    
def registrar_pedidos(df):
    try:
        last_row = len(base_len.get_values('a:A')) + 1
        last_lot = int(max(base_len.get_values('e2:e'))[0]) + 1
        now = (datetime.now() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        df['registro'] = now
        df['lote'] = last_lot
        df = df[['registro','Filial','Pedido','Transportadora','lote','Nota']]
        base_len.update(df.values.tolist(), 'a'+str(last_row),value_input_option='USER_ENTERED')
        return last_lot
    except Exception as e: 
        return str(e)

def consultar_pedidos_saida_loja(pedido=None, filial=0):
    df = pd.DataFrame(base_len.get_values('a2:h'))
    df = df[[0,1,2,3,4,5,6,7]]
    df.columns = ['Registro', 'Filial', 'Pedido', 'Transportadora', 'Lote', 'Nota', 'Ult_Atualização', 'Status']
    df['Pedido'] =  df['Pedido'].astype(str)
    df = df.loc[df['Filial'] == str(filial)]
    if pedido:
        return df.loc[df['Pedido'] == str(pedido)]
    else:
        return df

def transportadoras():
    transportadora = base_cad.get_values('e2:e')
    trans = []
    for tr in transportadora: 
        trans.append(tr[0])
    return trans
