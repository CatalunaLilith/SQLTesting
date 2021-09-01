# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:48:46 2021

@author: catal
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Numeric
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy.sql import text

# connect SQLAlchemy to DB
Base = declarative_base()

# # declare tables
# solar_system_objects = Table(
#     "solar_system_objects",
#     Base.metadata,
#     )

# moons_planets = Table(
#     "moons_planets",
#     Base.metadata,
#     Column("moon", Integer, ForeignKey("solar_system_objects.generated_id")),
#     Column("planet", Integer, ForeignKey("solar_system_objects.generated_id"))
#     )

# SQLAlchemy  models


class SolarSystemObjects(Base):
    __tablename__ = "solar_system_objects"
    generated_id = Column(Integer, primary_key=True)
    body = Column(String)
    mean_radius = Column(Numeric)
    mean_radius_rel = Column(Numeric)
    volume = Column(Numeric)
    volume_rel = Column(Numeric)
    mass = Column(Numeric)
    mass_rel = Column(Numeric)
    density = Column(Numeric)
    surface_gravity = Column(Numeric)
    surface_gravity_rel = Column(Numeric)
    type_of_object = Column(String)
    shape = Column(String)
    # moons_planets = relationship("MoonsPlanets",
    #                              back_populates="solar_system_objects")


class MoonsPlanets(Base):
    __tablename__ = "moons_planets"
    generated_id = Column(Integer, primary_key=True)
    moon_id = Column(Integer, ForeignKey("solar_system_objects.generated_id"))
    planet_id = Column(Integer, ForeignKey("solar_system_objects.generated_id"))
    # solar_system_objects = relationship("SolarSystemObjects",
    #                                     back_populates="moons_planets")
    moon = relationship("SolarSystemObjects", foreign_keys=[moon_id])
    planet = relationship("SolarSystemObjects", foreign_keys=[planet_id])


# connect SQLAlchemy to DB
engine = create_engine(r"sqlite:///C:\Users\catal\OneDrive\Desktop\Learning_to_Code\SQL\solar_system_2.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# run basic query with SQLAlchemy
# SELECT all
# print one field
# results = session.query(SolarSystemObjects).all()
# for row in results:
#     print(row.body)

# print all fields
# for row in results:
#     print({i.name: getattr(row, i.name) for i in row.__table__.columns})

# ORDER BY statement
# results2 = session.query(SolarSystemObjects).order_by(("surface_gravity"))
# for row in results2:
#     print({i.name: getattr(row, i.name) for i in row.__table__.columns})

# JOIN moons_planets to show body names
# SQL_double_join_names = 'SELECT S1.body, S2.body FROM moons_planets as MP \
#     JOIN solar_system_objects AS S1 ON MP.moon_id = S1.generated_id \
#         JOIN solar_system_objects AS S2 ON MP.planet_id = S2.generated_id'
# results3 = engine.execute(SQL_double_join_names)
# print("------------------------------")
# for row in results3:
#     print(row)
