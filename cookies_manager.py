import time
import zipfile
import shutil
import os
import base64

from dotenv import load_dotenv

from google_drive import download_file_by_name, upload_image_to_drive

load_dotenv()

WORKDIR = os.getenv("WORKDIR")
GCP_DEFAULT_FOLDER = os.getenv("GCP_DEFAULT_FOLDER")


def zip_folder(folder_path: str, output_path: str) -> None:
    shutil.make_archive(output_path, 'zip', folder_path)


def unzip_folder(zip_path: str, output_path: str) -> None:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)


def download_cookies(profile_id: str) -> None:
    base64_content = download_file_by_name(f'{profile_id}.zip', )
    with open(f'{WORKDIR}/{profile_id}.zip', 'wb') as file:
        file.write(base64.b64decode(base64_content))


def get_cookies(profile_id: str) -> str:
    try:
        download_cookies(profile_id)
        time.sleep(5)

        output_path = f'{WORKDIR}/{profile_id}'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        unzip_folder(f'{output_path}.zip', output_path)
        time.sleep(5)

        os.chmod(output_path, 0o777)

        return output_path
    except Exception as ex:
        print(f'--------- ERROR: {ex}')
        return 'No file'


def upload_cookies(profile_id: str) -> None:
    zip_folder(f'{WORKDIR}/{profile_id}', f'{WORKDIR}/{profile_id}')
    time.sleep(5)
    upload_image_to_drive(f'{WORKDIR}/{profile_id}.zip', )
