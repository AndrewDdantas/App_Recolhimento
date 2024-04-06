import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import timedelta, datetime


scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    './services/credentials.json', scope)

# Cria um serviço da API do Google Drive
drive_service = build('drive', 'v3', credentials=credentials)

client = gs.authorize(credentials)

sheet = client.open_by_key('1eqYyWwshEQPo0DpkhdgrG2ZLycJrj8kGprgRoHrnAGc')

base = sheet.worksheet('Base')

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

    base.update([[now,s.filial, s.pedido, s.pedido_novo, s.item, s.descricao, s.motivo, s.obs, s.destino, s.regiao, s.arquivo]], last_row)
    return 'Pedido Registrado'



def upload_arquivo(arquivo, nome):
    nome = str(nome)
    
    with open(nome + ".pdf", "wb") as f:
        f.write(arquivo.read())

    file_metadata = {'name': f'{nome}.pdf'}
    media = MediaFileUpload(nome + ".pdf", mimetype='application/pdf')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

  
    drive_service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    
    file_id = file.get('id')
    file_link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing' #link de compartilhamento

    return file_link


