from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

@csrf_exempt
def upload_to_google_drive(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            data = body.get('data')
            name = body.get('name')

            # Загрузка учетных данных из файла
            credentials = service_account.Credentials.from_service_account_file(
                'credentials.json', scopes=['https://www.googleapis.com/auth/drive']
            )

            service = build('drive', 'v3', credentials=credentials)

            # Создание Google Drive документа
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.document'
            }

            # Преобразование данных в поток BytesIO
            media = MediaIoBaseUpload(BytesIO(data.encode()), mimetype='text/plain', resumable=True)

            file = service.files().create(body=file_metadata, media_body=media).execute()

            return JsonResponse({'status': 'success', 'file_id': file['id']})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})