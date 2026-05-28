import uuid
from pathlib import Path
from fastapi import UploadFile


async def save_file(file: UploadFile) -> str:
    media_dir = Path("media/uploads")
    media_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename).suffix
    file_name = f"{uuid.uuid4().hex}{file_extension}"
    file_path = media_dir / file_name

    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return f"/media/uploads/{file_name}"
