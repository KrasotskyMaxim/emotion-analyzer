from fastapi import FastAPI, UploadFile, Request
from fastapi.templating import Jinja2Templates

from src import settings
from src.models import ApiModel


app = FastAPI()
templates = Jinja2Templates(directory=settings.TEMPLATE_PATH)
api_model = ApiModel()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})


@app.post("/process/")
async def process_image(file: UploadFile):
    content = await file.read()
    emotions = api_model.registrate_emotions(content)
    
    # return {file.filename: emotions}
    return {"filemane": file.filename, "result": emotions}