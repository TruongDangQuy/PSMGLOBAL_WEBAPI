from sqlalchemy import insert
from sqlalchemy.orm import Session

from . import models

def create_BaseEmployee(employee : dict, db: Session):
    db.execute(insert(models.BaseEmployee),employee)
    db.commit()
    return employee

def create_BaseTimeoff(timeoff : dict, db: Session):
    db.execute(insert(models.BaseTimeoff),timeoff)
    db.commit()
    return timeoff

def create_BaseTeam(team : dict, db: Session):
    db.execute(insert(models.BaseTeam),team)
    db.commit()
    return team

def create_BaseArea(area : dict, db: Session):
    db.execute(insert(models.BaseArea),area)
    db.commit()
    return area

def API_TD(area : dict, db: Session):
    db.execute(insert(models.API_TD),area)
    db.commit()
    return area