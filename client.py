import requests
import uvicorn
# from src import settings


# upload_url = ('/').join([settings.HOST_URL, 'process'])
# image_path = ('/').join([settings.STATIC_PATH, 'mask.jpg'])

# files = {"file": open(image_path, "rb")}

# response = requests.post(upload_url, files=files)
# print(response.json())

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)