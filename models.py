from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://admin:admin@localhost/newsdb"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(Text)
    publication_date = Column(DateTime)
    source_url = Column(String)
    category = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
