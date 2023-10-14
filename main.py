import time
timestr = time.strftime("%Y%m%d-%H%M%S")
from fastapi import FastAPI, File, UploadFile
import json
from fastapi.exceptions import HTTPException
import os
import yaml
from fastapi.responses import FileResponse
app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
@app.get("/")
def root():
    return {"hello":"welcome"}


@app.post("/file/upload")
def upload_file(file : UploadFile):
    if file.content_type != "application/json":
        raise HTTPException(400, detail="invalid Document type")
    data = json.loads(file.file.read())
    return {"content ":data, "filename":file.filename}
@app.post("/file/download")
def download(file: UploadFile):
    """Return a YAML file for the upload of a json file"""  
    if file.content_type != "application/json":
        raise HTTPException(400, detail="invalid Document type")
    else:
        json_data = json.loads(file.file.read())
        new_filename = "{}_{} .yaml".format(os.path.splitext(file.filename)[0], timestr)

        SAVE_FILE_PATH = os.path.join (UPLOAD_DIR, new_filename)
        with open(SAVE_FILE_PATH, "w") as f:
            yaml.dump(json_data, f)
        return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_filename)