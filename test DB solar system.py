# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 12:14:23 2021

@author: catal
"""

import sqlite3
conn = sqlite3.connect('solar_system_2.db')
c = conn.cursor()

# # CREATE table SOLAR_SYSTEM_OBJECTS
# c.execute("""CREATE TABLE solar_system_objects(
#   [generated_id] INTEGER PRIMARY KEY
# , [body] TEXT
# , [mean_radius] NUMERIC
# , [mean_radius_rel] NUMERIC
# , [volume] NUMERIC
# , [volume_rel] NUMERIC
# , [mass] NUMERIC
# , [mass_rel] NUMERIC
# , [density] NUMERIC
# , [surface_gravity] NUMERIC
# , [surface_gravity_rel] NUMERIC
# , [type_of_object] TEXT
# , [shape] TEXT
# )""")


def loadSQLStatments(file_name):
    """assumes file_name is an accessible .txt file composed of characters and line breaks
    returns a list of strings, each string being a line from the input file
    """
    file = open(file_name)
    file_holder = file.readlines()
    # remove last 5 char of each line
    file_holder = file_holder[3:]
    file_holder = [line[:-6] for line in file_holder]
    file.close()
    return file_holder


# INSERT statements from file
# insert_statements = loadSQLStatments("SQL solar system raw insert statements.rtf")
# for statement in insert_statements:
#     c.execute(statement)

# print all rows
# for row in c.execute('SELECT * FROM solar_system_objects'):
#     print(row)

# CREATE table moons_planets
# c.execute("""CREATE TABLE moons_planets(
#   [generated_id] INTEGER PRIMARY KEY
# , [moon_id] INTEGER
# , [planet_id] INTEGER
# )""")

# find and INSERT moon_planet data
# view3 = c.execute("SELECT a.generated_id,  b.generated_id \
#                     FROM solar_system_objects AS a \
#                     INNER JOIN solar_system_objects AS b \
#                     ON SUBSTR(a.type_of_object,14) = b.body \
#                     WHERE a.type_of_object LIKE 'satellite%'")
# for row in view3:
#     c.execute("INSERT INTO moons_planets (moon_id, planet_id) VALUES (?,?)",
#               (row[0], row[1]))

# classic sql join statement
# for row in c.execute('SELECT S1.body, S2.body FROM moons_planets as MP JOIN solar_system_objects AS S1 ON MP.moon_id = S1.generated_id JOIN solar_system_objects AS S2 ON MP.planet_id = S2.generated_id'):
#     print(row)

# make dynamic query with placeholders
variables = ['<', '=', '>']
for variable in variables:
    results = c.execute('SELECT S.body, S.mean_radius FROM solar_system_objects \
                        AS S WHERE S.mean_radius' + variable + ' 10000 \
                            ORDER BY S.mean_radius')
    for result in results:
        print(result)
    print("-------------------------------------------")


conn.commit()
conn.close()
