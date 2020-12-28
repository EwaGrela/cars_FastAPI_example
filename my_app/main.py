from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session


from my_app import crud, models, schemas, helpers, config
from my_app.database import declarative_base, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return {"sanity_check": "Hello world"}


@app.get("/cars", response_model=List[schemas.Car])
def cars(db: Session = Depends(get_db)):
    cars = crud.get_cars(db)
    return cars


@app.get("/cars/{car_id}", response_model=schemas.Car)
def car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Such car was not found")
    return car

@app.delete("/cars/{car_id}", response_model=schemas.Car)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="No such car")
    crud.delete_car(db, car)


@app.post("/cars", response_model=schemas.CarBase)
def add_car(car: schemas.CarBase, db: Session = Depends(get_db)):
    data = {}
    data["make"], data["model"] = car.make, car.model
    found_car = crud.get_car_by_type(db, car.make, car.model)
    if found_car:
        raise HTTPException(status_code=400, detail="Car already in db")
    res = helpers.get_external_data(data)

    if res:
        crud.create_car(db, car)
    else:
        raise HTTPException(
            status_code=404,
            detail="No such car in external db")


@app.put("/rate", response_model=schemas.Rate)
def rate(rate: schemas.Rate, db: Session = Depends(get_db)):
    found_car = crud.get_car_by_type(db, rate.make, rate.model)
    if not found_car:
        raise HTTPException(status_code=404, detail="No such car")
    crud.rate_car(db, rate)


@app.get("/popular")
def popular(db: Session = Depends(get_db)):
    popular_cars = crud.get_popular_cars(db)
    return popular_cars
