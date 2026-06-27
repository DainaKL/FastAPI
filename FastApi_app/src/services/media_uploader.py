import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from src.core.config import settings

MEDIA_ROOT = Path(settings.MEDIA_DIR)


def get_upload_path(folder: str, filename: str) -> Path:
    ext = filename.split('.')[-1] if '.' in filename else 'jpg'
    unique_name = f"{uuid.uuid4()}.{ext}"
    
    folder_path = MEDIA_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    
    return folder_path / unique_name


async def save_avatar(file: UploadFile) -> str:
    path = get_upload_path('avatars', file.filename)
    content = await file.read()
    with open(path, 'wb') as f:
        f.write(content)
    return str(path.relative_to(MEDIA_ROOT))


async def save_post_image(file: UploadFile) -> str:
    path = get_upload_path('post_images', file.filename)
    content = await file.read()
    with open(path, 'wb') as f:
        f.write(content)
    return str(path.relative_to(MEDIA_ROOT))


async def save_comment_image(file: UploadFile) -> str:
    path = get_upload_path('comment_images', file.filename)
    content = await file.read()
    with open(path, 'wb') as f:
        f.write(content)
    return str(path.relative_to(MEDIA_ROOT))


async def save_file(file: UploadFile, entity_type: str = 'temp') -> str:
    if entity_type == 'user':
        return await save_avatar(file)
    elif entity_type == 'post':
        return await save_post_image(file)
    elif entity_type == 'comment':
        return await save_comment_image(file)
    else:
        path = get_upload_path('temp', file.filename)
        content = await file.read()
        with open(path, 'wb') as f:
            f.write(content)
        return str(path.relative_to(MEDIA_ROOT))


def delete_file(relative_path: str) -> bool:
    if not relative_path:
        return False
    
    full_path = MEDIA_ROOT / relative_path
    if full_path.exists() and full_path.is_file():
        full_path.unlink()
        return True
    return False


def get_file_path(relative_path: str) -> Optional[Path]:
    full_path = MEDIA_ROOT / relative_path
    if full_path.exists():
        return full_path
    return None
