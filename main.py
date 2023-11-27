from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from PIL import Image
import requests
from io import BytesIO

# Models
from models.Extractor import Data_Extraction
from models.Aadhaar import Aadhaar_OCR
from models.PanCard import Pan_OCR


class InvoiceModel(BaseModel):
  key: str
  urls: list

class AadhaarModel(BaseModel):
  key: str
  url: str

class PanModel(BaseModel):
  key: str
  url: str

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello World"}


@app.post("/get_data")
async def get_data(data: InvoiceModel) -> dict:
  key = data.key

  if key != "aiwapi12345":
    raise HTTPException(status_code=400, detail="Error in authenticating user")
  print("get key")
  images=[]

  final_dict = dict(data)['urls']
  print(final_dict)

  if len(final_dict) < 1:
    raise HTTPException(status_code=400, detail="Empty dictionary")

  for i,j in enumerate(final_dict):
    img=requests.get(j)
    images.append(Image.open(BytesIO(img.content)))

  extractor=Data_Extraction(images)
  result=extractor.combined_data()

  return {
    "message": "API working successfully",
    "result": result
  }


@app.post("/get-aadhaar-details")
async def get_aadhaar_details(data: AadhaarModel) -> dict:
  key = data.key
  aadhaar_img = data.url

  if key != "aiwapi12345":
    raise HTTPException(status_code=400, detail="Error in authenticating user")

  response = requests.get(aadhaar_img)
  if response.status_code != 200:
    raise HTTPException(status_code=400, detail="image not fetched")
  
  ocr = Aadhaar_OCR(aadhaar_img)

  data = ocr.extract_data()
  return {
    "message": "Aadhaar Card Data fetched successfully",
    "result": data
  }

  
@app.post("/get-pan-details")
async def get_pan_details(data: PanModel) -> dict:
  key = data.key
  pan_img = data.url

  if key != "aiwapi12345":
    raise HTTPException(status_code=400, detail="Error in authenticating user")

  response = requests.get(pan_img)
  if response.status_code != 200:
    raise HTTPException(status_code=400, detail="image not fetched")
  
  ocr = Pan_OCR(pan_img)

  data = ocr.extract_data()
  return {
    "message": "Pan Card Data fetched successfully",
    "result": data[0]
  }