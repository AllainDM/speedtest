import uvicorn
from fastapi import FastAPI, Response
from starlette.background import BackgroundTask

import io

import config

app = FastAPI()

# Определяем размер виртуального файла
VIRTUAL_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

@app.get("/download")
async def download_file():
    """
    Отправляет большой объем данных клиенту.
    """
    # Создаем "виртуальный" файл размером 100 МБ из нулей
    # (для теста можно увеличить размер)
    # ВАЖНО: Создаем его внутри функции, чтобы каждый запрос получал новый, открытый файл
    data = io.BytesIO(b'\x00' * VIRTUAL_FILE_SIZE)

    # Перемещаем указатель в начало "файла" для повторного чтения
    # (хотя для только что созданного файла он уже в начале)
    data.seek(0)

    # Создаем Response с данными. media_type="application/octet-stream"
    # указывает, что это бинарные данные.
    response = Response(
        content=data.read(),
        media_type="application/octet-stream"
    )

    # Используем BackgroundTask для закрытия виртуального файла.
    # Это хорошая практика для освобождения ресурсов после отправки ответа.
    response.background = BackgroundTask(data.close)

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)