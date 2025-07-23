from fastapi import FastAPI, UploadFile, File
import whisper
import uvicorn
import tempfile
import shutil

app = FastAPI()
model = whisper.load_model("base")  # Можно "tiny", "base", "small", "medium", "large"

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    return {"text": result["text"]}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
