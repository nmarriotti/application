import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef_users import *
 
engine = create_engine('sqlite:///data.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password",1)
session.add(user)
 
user = User("test","test",0)
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()
