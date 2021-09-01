# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 13:46:05 2021

@author: catal
"""
import pdb
import sys
import sqlite3
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel


# pdb.set_trace()
# print(list(map(str, QSqlDatabase.drivers())))
# print(((QSqlDatabase.drivers())))


# Create the connection
con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("solar_system_objects.sqlite")

print(list(map(str, QSqlDatabase.drivers())))
print(((QSqlDatabase.drivers())))

# # Create the application
app = QApplication(sys.argv)


# Try to open the connection, and handle possible errors
if not con.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % con.lastError().databaseText(),
    )
    sys.exit(1)

# Create the application's window
win = QLabel("Connection Successfully Opened!")
win.setWindowTitle("App Name")
win.resize(200, 100)
win.show()
sys.exit(app.exec_())

# # Open the connection and handle errors
# if not con.open():
#       print("Unable to connect to the database")
#       sys.exit(1)
     
#TODO figure out why no db connection
#try loading file that worked another day, if still works comapre code 