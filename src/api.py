from fastapi import FastAPI, UploadFile, Request
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
from src import settings
from src.models import ApiModel

import json

app = FastAPI()
app.mount(
    "/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=settings.TEMPLATE_PATH)
api_model = ApiModel()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})


@app.get("/test/")
async def home(request: Request):
    return {"status": "ok"} 



@app.post("/process/")
async def process_image(files: List[UploadFile]):
    if not files:
        return []
    
    response = {}
    for file in files:
        content = await file.read()
        emotions = api_model.registrate_emotions(content)
        response[file.filename] = emotions
        api_model.load_image(file.filename, content)
    api_model.process_images()
    # plot_image = api_model.plots[0].image.tobytes()
    img_obj = api_model.plots[0]
    print(os.getcwd())
    img_obj.image.save(f"static/{img_obj.name}")
    print("Yes")
    return {'status': 'ok'}