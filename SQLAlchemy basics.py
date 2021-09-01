# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 19:34:20 2021

@author: catal
"""

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy import tuple_
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.sql import text, bindparam

engine = create_engine('sqlite:///:memory:', echo=True)  # echo=False less verbose
# engine is core interface to the DB

# Define and Create Tables
metadata = MetaData()  # the database = collection of tables
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('fullname', String),
              )
addresses = Table('addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', None, ForeignKey('users.id')),
                  Column('email_address', String, nullable=False)
                  )

# to CREATE TABLE in DB, for all Table objects
metadata.create_all(engine)

# Insert Expressions
ins = users.insert()  # insert construct format table_name.insert(values)
ins = users.insert().values(name='jack', fullname='Jack Jones')
# to explicitly insert values
str(ins)  # str() function to see content of a construct

# Executing expressions
conn = engine.connect()  # to aquire connection
# Connection object reps an actively checked out DBAPI connection resource
result = conn.execute(ins)  # to execute expression, returns cursor-like object
result.inserted_primary_key  # to get primary keys in result

# standard single statement execution
ins = users.insert()
conn.execute(ins, {"id": 2, "name": "wendy", "fullname": "Wendy Williams"})

# Executing Multiple Statements
# execute list of dicts each containing a set of parameters to be inserted
conn.execute(addresses.insert(), [
        {'user_id': 1, 'email_address': 'jack@yahoo.com'},
        {'user_id': 1, 'email_address': 'jack@msn.com'},
        {'user_id': 2, 'email_address': 'www@www.org'},
        {'user_id': 2, 'email_address': 'wendy@aol.com'},
        ])  # depends on SQLite to generate primary key
# each dict must have the same set of keys
# simillarly can execute many insert(), update() and delete() constructs

# Selecting
s = select([users])  # basic select() call, returns cursor with row objects
# each row = tuple, comma seperated fields
result = conn.execute(s)
# to simply print results of a select statement
for row in result:
    print(row)
# to pythonically access cursor contents with tuple assignment
for id, name, fullname in result:
    print("name:", name, "; fullname: ", fullname)

# Selecting Specific Columns
s = select(users.c.name, users.c.fullname)  # format table_name.c.column_name
# c is column attribute of table
result = conn.execute(s)
# if two tables in select(), returns cartesian product
# WHERE clause acting like a left join
s = select(users, addresses).where(users.c.id == addresses.c.user_id)

# Operators
# the Operators.op() method generates whatever operator you need
print(users.c.name.op('tiddlywinks')('foo'))

# Commonly Used Operators
# ColumnOperators.__eq__()
select.where(users.c.name == 'ed')
# ColumnOperators.__ne__()
select.where(users.c.name != 'ed')
# ColumnOperators.like() (maybe case sensitive depending on backend)
select.where(users.c.name.like('%ed%'))
# ColumnOperators.ilike() (case-insensitive LIKE on all backends)
select.where(users.c.name.ilike('%ed%'))
# ColumnOperators.in_()
select.where(users.c.name.in_(['ed', 'wendy', 'jack']))
# in_() works with Select objects too:
select.where.filter(users.c.name.in_(
    select(users.c.name).where(users.c.name.like('%ed%'))))
# use tuple_() for composite (multi-column) queries
select.where(tuple_(users.c.name, users.c.nickname).
             in_([('ed', 'edsnickname'), ('wendy', 'windy')])
             )
# ColumnOperators.not_in()
select.where(~users.c.name.in_(['ed', 'wendy', 'jack']))
# ColumnOperators.is_()
# select.where(users.c. == None)
# ColumnOperators.is_not()
select.where(users.c.name != "")
# use and_() (NOT python and)
select.where(and_(users.c.name == 'ed', users.c.fullname == 'Ed Jones'))
# (like and) or send mutiple expressions to .where()
select.where(users.c.name == 'ed', users.c.fullname == 'Ed Jones')
# ColumnOperators.match()
select.where(users.c.name.match('wendy'))

# Conjunctions
# beware parans b/c Python precedence rules
print(and_(
         users.c.name.like('j%'),
         users.c.id == addresses.c.user_id,
         or_(
              addresses.c.email_address == 'wendy@aol.com',
              addresses.c.email_address == 'jack@yahoo.com'
         ),
         not_(users.c.id > 5)
       )
      )

# Using Textual SQL
# w/ bound parameters are specified in text() using the named colon format
s = text(
     "SELECT users.fullname || ', ' || addresses.email_address AS title "
     "FROM users, addresses "
     "WHERE users.id = addresses.user_id "
     "AND users.name BETWEEN :x AND :y "
     "AND (addresses.email_address LIKE :e1 "
     "OR addresses.email_address LIKE :e2)")
conn.execute(s, {"x": "m", "y": "z", "e1": "%@aol.com", "e2": "%@msn.com"}).fetchall()

# Specifying Bound Parameter Behaviors
# pre-established bound values w/ TextClause.bindparams()
stmt = text("SELECT * FROM users WHERE users.name BETWEEN :x AND :y")
stmt = stmt.bindparams(x="m", y="z")
# or explicitly typed bound values
stmt = stmt.bindparams(bindparam("x", type_=String), bindparam("y", type_=String))
result = conn.execute(stmt, {"x": "m", "y": "z"})

# Specifying Result-Column Behaviors
# TextClause.columns() method to specify the return types, based on name
stmt = stmt.columns(id=Integer, name=String)
# TextClause.columns() full column expressions positionally
stmt = text("SELECT id, name FROM users")
stmt = stmt.columns(users.c.id, users.c.name)
# returns a TextAsFrom object
# supports the full suite of TextAsFrom.c and other “selectable” operations
j = stmt.join(addresses, stmt.c.id == addresses.c.user_id)
new_stmt = select(stmt.c.id, addresses.c.id).select_from(j).where(stmt.c.name == 'x')
# use column expressions directly
stmt = text("SELECT users.id, addresses.id, users.id, "
            "users.name, addresses.email_address AS email "
            "FROM users JOIN addresses ON users.id=addresses.user_id "
            "WHERE users.id = 1").columns(
                users.c.id,
                addresses.c.id,
                addresses.c.user_id,
                users.c.name,
                addresses.c.email_address
                )
result = conn.execute(stmt)

# Using text() fragments inside bigger statements
# select() objects accept text() objects as argument for its builder functions
s = select(
            text("users.fullname || ', ' || addresses.email_address AS title")
         ).\
             where(
                 and_(
                     text("users.id = addresses.user_id"),
                     text("users.name BETWEEN 'm' AND 'z'"),
                     text(
                         "(addresses.email_address LIKE :x "
                         "OR addresses.email_address LIKE :y)")
                     )
                 ).select_from(text('users, addresses'))
conn.execute(s, {"x": "%@aol.com", "y": "%@msn.com"}).fetchall()

# Using Aliases and Subqueries
#  FromClause.alias() method on table or From Clause, returns Alias object
# Alias object refers to a mapping of Column objects
a1 = addresses.alias()
























