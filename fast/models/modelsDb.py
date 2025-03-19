from db.connection import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__= "Users"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    name=Column(String)
    age=Column(Integer)
    email=Column(String)