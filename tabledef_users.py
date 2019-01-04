from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	cred = Column(Boolean)

	def __init__(self, username, password, cred):
		self.username = username
		self.password = password
		self.cred = cred

#create tables
Base.metadata.create_all(engine)
