import base64
import os
from typing import List

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

load_dotenv()
SCOPES = {
    'drive': 'https://www.googleapis.com/auth/drive.file',
    'readonly': 'https://www.googleapis.com/auth/drive.readonly',
    'full': 'https://www.googleapis.com/auth/drive'
}
GCP_SERVICE_ACCOUNT_FILE_PATH = os.getenv("GCP_SERVICE_ACCOUNT_FILE_PATH")
GCP_SERVICE_SUBJECT = os.getenv("GCP_SERVICE_SUBJECT")
GCP_DEFAULT_FOLDER = os.getenv("GCP_DEFAULT_FOLDER")


#
def get_credentials(scopes: List) -> service_account.Credentials:
    target_scopes = [SCOPES[scope] for scope in scopes]
    source_credentials = service_account.Credentials.from_service_account_file(
        GCP_SERVICE_ACCOUNT_FILE_PATH, scopes=target_scopes, subject=GCP_SERVICE_SUBJECT
    )
    return source_credentials


def build_drive_service(scope: str) -> build:
    creds = get_credentials([scope])
    return build('drive', 'v3', credentials=creds)


def upload_image_to_drive(image_path: str) -> str:
    drive_service = build_drive_service('drive')

    file_metadata = {
        'name': os.path.basename(image_path),
        'parents': [GCP_DEFAULT_FOLDER]
    }

    media = MediaFileUpload(image_path, resumable=True)
    try:
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='webContentLink'
        ).execute()

        return file.get('webContentLink').replace('&export=download', '')
    except (TimeoutError, HttpError):
        return 'File upload timeout error'


def get_all_files(folder_id: str) -> List[dict]:
    service = build_drive_service('readonly')
    query = f"'{folder_id}' in parents"

    results = service.files().list(q=query, fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])

    while 'nextPageToken' in results:
        results = service.files().list(q=query, fields='nextPageToken, files(id, name)',
                                       pageToken=results['nextPageToken']).execute()
        items.extend(results.get('files', []))

    return items


def download_file_by_name(file_name: str) -> str:
    drive_service = build_drive_service('full')
    files = get_all_files(GCP_DEFAULT_FOLDER)
    file_id = None
    for file in files:
        if file['name'] == file_name:
            file_id = file['id']
            break

    if not file_id:
        return 'File not found'

    request = drive_service.files().get_media(fileId=file_id)
    downloaded = request.execute()

    base64_content = base64.b64encode(downloaded).decode()
    return base64_content
