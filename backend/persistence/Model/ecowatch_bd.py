from sqlalchemy import ForeignKey, Text, DateTime, CHAR, Float, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship, declarative_base, backref, Mapped


from typing import List
from datetime import datetime

Base = declarative_base()

class Query(Base):
    __tablename__ = "queries"

    query_id : Mapped[str] = mapped_column(primary_key=True)
    table : Mapped[str] = mapped_column(primary_key=True)
    device_ID : Mapped[str] = mapped_column( CHAR(14), nullable=True)
    
    latest_query_call : Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                        nullable=False, 
                                                        server_default=func.now(), 
                                                        onupdate=func.now())
    
    def __repr__(self):
        return f"query_id={self.query_id}, latest_call={self.latest_query_call}, response={self.response} "


class Climatrack(Base):
    __tablename__ = "climatrack"

    id : Mapped[int] = mapped_column(primary_key=True)
    ID_boitier : Mapped[str] = mapped_column(CHAR(14), primary_key=True)
    timestamp : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    humidity : Mapped[float] = mapped_column(Float, nullable=True)
    temperature : Mapped[float] = mapped_column(Float, nullable=True)
    tvoc : Mapped[int] = mapped_column(Integer, nullable=True)
    co2 : Mapped[int] = mapped_column(Integer, nullable=True)
    pm1_0:Mapped[str] = mapped_column(Text, nullable=True)
    pm10:Mapped[str] = mapped_column(Text, nullable=True)
    pm2_5:Mapped[str] = mapped_column(Text, nullable=True)
    sound_level: Mapped[float] = mapped_column(Float, nullable=True)
    

class Aquacheck(Base):
    __tablename__ = "aquacheck"

    id : Mapped[int] = mapped_column(primary_key=True)
    ID_boitier : Mapped[str] = mapped_column(CHAR(14), primary_key=True)
    timestamp : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    humidity : Mapped[float] = mapped_column(Float, nullable=True)
    temperature : Mapped[float] = mapped_column(Float, nullable=True)
    ground_humidity : Mapped[float] = mapped_column(Float, nullable=True)
    humidex : Mapped[float] = mapped_column(Float, nullable=True)
    


class Conversation(Base):
    __tablename__ = "conversations"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id : Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at : Mapped[str] = mapped_column(Text, nullable=False)

    messages : Mapped[List["Message"]] = relationship( back_populates="conversation" )

    def __repr__(self):
        return f"id={self.id}, session_id={self.session_id}, created_at={self.created_at}"


class Message(Base):
    __tablename__ = "messages"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id = mapped_column( ForeignKey("conversations.id"), nullable=False, index=True)
    role : Mapped[str] = mapped_column(Text, nullable=False )
    content : Mapped[str] = mapped_column( nullable=False )
    timestamp : Mapped[str] = mapped_column( nullable=False )

    conversation : Mapped[Conversation] = relationship( back_populates="messages" )

    def __repr__(self):
        return f"id={self.id}, conversation_id={self.conversation_id}, role={self.role}, content={self.content}, timestamp={self.timestamp} "
