from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from typing import List
from datetime import datetime

engine = create_engine("sqlite+pysqlite:///ecowatch.db", echo=True)

Base = declarative_base()

class Query(Base):
    __tablename__ = "queries"

    query_id : Mapped[str] = mapped_column(primary_key=True)
    latest_query_call : Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                        nullable=False, 
                                                        server_default=func.now(), 
                                                        onupdate=func.now())
    response : Mapped[str] = mapped_column(nullable=False) 

class Conversation(Base):
    __tablename__ = "conversations"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id : Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at : Mapped[str] = mapped_column(Text, nullable=False)

    messages : Mapped[List["Message"]] = relationship( back_populates="conversation" )

class Message(Base):
    __tablename__ = "messages"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id = mapped_column( ForeignKey("conversations.id"), nullable=False, index=True)
    role : Mapped[str] = mapped_column(Text, nullable=False )
    content : Mapped[str] = mapped_column( nullable=False )
    timestamp : Mapped[str] = mapped_column( nullable=False )

    conversation : Mapped[Conversation] = relationship( back_populates="messages" )


Base.metadata.create_all(engine)