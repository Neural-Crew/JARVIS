from sqlalchemy import create_engine
from backend.persistence.Model.ecowatch_bd import Base

engine = create_engine("sqlite+pysqlite:///ecowatch.db", echo=False)
Base.metadata.create_all(engine)
