from fastapi import FastAPI, File, UploadFile
import shutil
import os
from fraud_detector import analyze_document

app = FastAPI(title="ID Forgery Risk Analyzer")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "ID Forgery Risk Analyzer is running"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    report = analyze_document(file_path)
    return {
        "filename": file.filename,
        "report": report
    }