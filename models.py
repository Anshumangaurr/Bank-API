from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    branch = Column(String)
    ifsc = Column(String)
    address = Column(String)
    bank_id = Column(Integer, ForeignKey("banks.id"))

    bank = relationship("Bank")


import os

# prefer database URL from environment (Heroku sets DATABASE_URL)
db_url = os.environ.get("DATABASE_URL", "sqlite:///bank.db")
engine = create_engine(db_url)


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def seed_data():
    """Insert a couple of banks/branches if the database is empty.
    This helper is used by tests or during development to ensure there
    is something to query.
    """
    # only seed once when there are no banks present
    if session.query(Bank).count() > 0:
        return

    b = Bank(name="Example Bank")
    session.add(b)
    session.commit()

    branches = [
        Branch(branch="Main", ifsc="EXAMP001", address="100 Example Ln", bank=b),
        Branch(branch="West", ifsc="EXAMP002", address="200 Example Ave", bank=b),
    ]
    session.add_all(branches)
    session.commit()

    print("seeded sample data")
