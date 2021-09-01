# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 17:13:00 2021

@author: catal
"""
#to setup sqlite3 server 

import sqlite3
from sqlite3 import Error



connection = sqlite3.connect("aquarium.db")
print(connection.total_changes)

cursor = connection.cursor()
# cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")

cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
print(connection.total_changes)

target_fish_name = "Jamie"
rows = cursor.execute(
    "SELECT name, species, tank_number FROM fish WHERE name = ?",
    (target_fish_name,),
).fetchall()
print(rows)

new_tank_number = 2
moved_fish_name = "Sammy"
cursor.execute(
    "UPDATE fish SET tank_number = ? WHERE name = ?",
    (new_tank_number, moved_fish_name)
)
rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)








