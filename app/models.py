from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass    

db = SQLAlchemy(model_class=Base)

    
class Customer(Base):
    __tablename__ = 'customers'
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    phone: Mapped[int] = mapped_column(db.String(20), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False) 
    
    services: Mapped[List["Service"]] = db.relationship(back_populates='customer')
    
class Mechanic(Base):
    __tablename__ = 'mechanics'
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    salary: Mapped[int] = mapped_column(db.String(20), nullable=False)
    phone: Mapped[int] = mapped_column(db.String(20), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    
    services: Mapped[List["Service"]] = db.relationship(secondary='service_mechanic', back_populates='mechanics')

class Service(Base):
    __tablename__ = 'services'
    id:Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date]= mapped_column(db.Date, nullable=False)
    desc: Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    vin_number: Mapped[str] = mapped_column(db.String(20), nullable=False, unique=True)
    
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary='service_mechanic', back_populates='services')
    customer: Mapped["Customer"] = db.relationship(back_populates='services')

service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('service_id', db.Integer, db.ForeignKey('services.id')),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'))
)