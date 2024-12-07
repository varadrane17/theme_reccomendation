import requests
import uvicorn
from fastapi import FastAPI
import base64
from PIL import Image
import json
from io import BytesIO
from pydantic import BaseModel
app = FastAPI()

with open('themes.txt', 'r') as file:
    global themes
    themes = file.read().splitlines()

def url_to_img(img_url: str) -> Image.Image:
    return Image.open(BytesIO(requests.get(img_url).content))

def get_object_from_image(input_image_url):

    inp=url_to_img(input_image_url)
    url = 'https://static-aws-ml1.phot.ai/blip'
    headers = {"Content-Type": "application/json"}
    buffered = BytesIO()
    inp.thumbnail((1024, 1024))
    inp.save(buffered, format="JPEG")
    inp_base64 = base64.b64encode(buffered.getvalue())
   
    data = {
            "image":inp_base64.decode(),        
        }
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    k = response.text
    k = json.loads(k)
    return k['objec']

class Theme(BaseModel):
    input_image_url: str
    theme_count: int

@app.get("/server_status")
def root():
    return {"message": "Server is running"}

@app.post("/get_theme")
def get_theme(request: Theme):
    product_description=get_object_from_image(request.input_image_url)
    url = "http://localhost:11434/api/chat"
    data = {
    "model": "llama3.2",
    "messages": [
            { "role": "user", "content": f"get the  best theme for the product description : ({product_description}) among the following themes for Background: {themes} . Only give the theme name in folowing format : [theme1, theme2, theme3 till theme{request.theme_count}]" }
        ],
    "stream": False
    }
    response = requests.post(url, json=data)
    response_json = response.json()['message']['content']
    theme = response_json.split('[')[1].split(']')[0].split(',')
    return theme
