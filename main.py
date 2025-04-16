from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
from inference import separate_vocals  # zakładamy, że generuje vocals i instrumental

app = FastAPI()

@app.post("/separate")
async def separate(file: UploadFile = File(...)):
    input_path = f"input_audio/{file.filename}"
    instrumental_path = f"output_audio/{file.filename}_instrumental.wav"

    os.makedirs("input_audio", exist_ok=True)
    os.makedirs("output_audio", exist_ok=True)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # uruchamiamy separację (funkcja tworzy vocals i instrumental)
    separate_vocals(input_path)

    # zwracamy instrumental
    return FileResponse(instrumental_path, media_type="audio/wav", filename="instrumental.wav")

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

