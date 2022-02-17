from sqlalchemy import Table, Column, Computed, String, Boolean, Integer, DateTime, MetaData, DATETIME
from resources import engine
meta = MetaData()

class ClockTable:
    tabela = Table("clock", meta,
                   Column("_ID", Integer, primary_key=True, autoincrement=True),
                   Column("username", String, nullable=False),
                   Column("email", String, nullable=False),
                   Column("pid", String, Computed(f"'select public_id from User where email=email'")),
                   Column("clockin", Integer),
                   Column("clockout", Integer),
                   Column("humanclockin", DateTime(timezone=True)),
                   Column("humanclockout", DateTime(timezone=True)),
                   Column("deltatrabalho", String, Computed('humanclockout-humanclockin', persisted=True)))

if __name__ == "__main__":
    meta.create_all(engine)
