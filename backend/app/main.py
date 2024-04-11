import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


from funcions.cian import findr
from funcions.model_func import Result_Maker, Result_Maker_MAX

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],)



@app.get('/')
def return_info():
    return 'Hello, stranger. Welcome to CIAN-based ML-service!'

#### /cian_id
class FindClass(BaseModel):
    find_me: str
class CianClass(BaseModel):
        total_area : float
        repair_type : str
        lat : float
        lan : float
        metro_dist : float
        metro : str
        kremlin_dist : float
        pred : float
        real : float
        link : str

@app.post('/cian_id')
def clf_text(data: FindClass):

    json = findr(data.find_me)
    
    response = CianClass(
        total_area = json['total_area'],
        repair_type = json['repair_type'],
        lat = json['lat'],
        lan = json['lan'],
        metro_dist= json['metro_dist'],
        metro= json['metro'],
        kremlin_dist = json['kremlin_dist'],
        pred = json['pred'],
        real = json['real'],
        link = json['link'],
        )
    return response


#### /classify
class Item(BaseModel):
    square: int
    quality: str
    lat: float
    lan: float
class ClassifyClass(BaseModel):
    classify_me: str
    metro_m : str


@app.post('/classify')
def classify(data: Item):

    square = int(data.square)
    quality = data.quality
    lat = float(data.lat)
    lan = float(data.lan)

    json = {'square':square,'quality':quality,'lat':lat,'lan':lan}

    result = Result_Maker(json)
    response = ClassifyClass(
        classify_me = str(result[0]),
        metro_m     = str(result[-1]))
    
    return response


#### /classify_max
class Property(BaseModel):
    total_area: float
    room_count: int
    material_type: str
    repair_type: str
    floor: int
    floors_count: int
    metro: str
    build_year: int
    combined_wcs_count: int
    ceiling_height: float
    house_heating_supply: str
    loggiascount: int
    latitude: float
    longitude: float
    okrug: str
    offer_type: str
    city: str
    raion: str
    street: str
    house: str
    id: int
    phone: str
    flat_type: str
    is_apartment: int
    is_penthause: int
    living_area: float
    kitchen_area: float
    all_rooms_area: float
    price: int
    currency: str
    house_material_type: str
    edit_time: str
    publication_date: int
    house_material_bti: str
    is_emergency: int
    house_overlap_type: str
    metro_time: int
    travel_type: str

class ClassifyMaxClass(BaseModel):
    pred: int


@app.post("/classify_max")
def classify_max(data: Property):

    price = Result_Maker_MAX(data)

    response = ClassifyMaxClass(
        pred = price)
    
    return response

##### run from api folder:
##### uvicorn app.main:app
##### export PYTHONPATH=$PYTHONPATH:/