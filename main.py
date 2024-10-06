from fastapi import FastAPI, HTTPException
from models import SessionLocal, Weather
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="API de Dados Climáticos")

class WeatherSchema(BaseModel):
    id: int
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    timestamp: datetime

    class Config:
        orm_mode = True

@app.get("/weather/", response_model=List[WeatherSchema])
def read_weather():
    session = SessionLocal()
    dados = session.query(Weather).all()
    session.close()
    return dados

@app.get("/weather/{weather_id}", response_model=WeatherSchema)
def read_weather_item(weather_id: int):
    session = SessionLocal()
    dado = session.query(Weather).filter(Weather.id == weather_id).first()
    session.close()
    if dado:
        return dado
    else:
        raise HTTPException(status_code=404, detail="Dados não encontrados")
