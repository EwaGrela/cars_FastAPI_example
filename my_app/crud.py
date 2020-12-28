from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import Session

from my_app import models, schemas


def get_cars(db: Session):
    return db.query(models.Car).all()


def get_car_by_id(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def get_car_by_type(db: Session, car_make: str, car_model: str):
    found_car = db.query(
        models.Car).filter(
        models.Car.make == car_make).filter(
            models.Car.model == car_model).first()
    return found_car


def create_car(db: Session, car: schemas.CarBase):
    new_car = models.Car(make=car.make, model=car.model)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


def rate_car(db: Session, rate: schemas.Rate):
    car_to_rate = db.query(
        models.Car).filter(
        models.Car.make == rate.make).filter(
            models.Car.model == rate.model).first()
    car_to_rate.rates_number += 1
    car_to_rate.rates_sum += rate.score
    car_to_rate.average_rate = car_to_rate.rates_sum / car_to_rate.rates_number
    db.commit()
    db.refresh(car_to_rate)
    return car_to_rate


def get_popular_cars(db: Session):
    popular_cars = db.query(
        models.Car).order_by(
        models.Car.rates_number.desc()).all()
    return popular_cars


def delete_car(db: Session, car: schemas.Car):
    db.delete(car)
    db.commit()

