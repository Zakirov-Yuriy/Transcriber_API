from fastapi import FastAPI, UploadFile, File
import whisper
import uvicorn
import tempfile
import shutil
import os

app = FastAPI()
model = whisper.load_model("tiny")  # Можно выбрать и другой: "base", "small", "medium", "large"


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Получаем расширение файла, например .mp3, .mp4, .wav
    suffix = os.path.splitext(file.filename)[1]

    # Создаём временный файл с тем же расширением
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    print(f"[Server] Принят файл: {file.filename}, сохранён как: {tmp_path}")
    result = model.transcribe(tmp_path)

    # (необязательно) можно удалить временный файл после использования
    os.remove(tmp_path)

    return {"text": result["text"]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
