from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, DateTime, ForeignKey, Computed
from resources import *
from resources import engine
meta = MetaData()

tabela = Table("user", meta,
    Column("id",Integer, primary_key=True),
    Column("username",String, unique=True, nullable=False),
    Column("name",String, nullable=False),
    Column("email",String, unique=True, nullable=False),
    Column("role",String, default='cliente'),
    Column("public_id",String, nullable=False, unique=True),
    Column("dog",String),
    Column("date",Date),
    Column("dateandtime",DateTime))

if __name__ == "__main__":
    meta.create_all(engine)