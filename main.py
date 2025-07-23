from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisper
import os
import tempfile

app = FastAPI()

# Загружаем легкую модель (можно "base", "small", но "tiny" быстрее и легче)
model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)
        os.remove(tmp_path)
        return {"text": result["text"]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
