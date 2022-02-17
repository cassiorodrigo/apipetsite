from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, DateTime, ForeignKey
from resources import *


class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    date = Column(Date)
    dateandtime = Column(DateTime)

if __name__ == "__main__":
    hoje = date.today()
    agora = datetime.now()
    db.create_all()
    user = User(date=hoje, dateandtime=agora, username='cassiorodrigo', email="cassiorodrigo@gmail.com")
    db.session.add(user)
    db.session.commit()
    res = User.query.all()
    print(datetime.timestamp(res[0].dateandtime))

