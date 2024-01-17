from fastapi import FastAPI, File, UploadFile
import uvicorn
from asr_model import Whisper_Model
import os


app = FastAPI()
asr_model = Whisper_Model()

@app.post("/asr_from_file")
def read_item(audio_file: UploadFile):
    file_path = f"./uploads/{audio_file.filename}"
    with open(file_path,'wb') as f:
        f.write(audio_file.file.read())
    text = asr_model.infer(file_path)
    os.remove(file_path)
    return {"file_name": audio_file.filename,"text": text}

if __name__ == "__main__":
    config = uvicorn.Config("asr_api:app", port=1901, log_level="info",host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()