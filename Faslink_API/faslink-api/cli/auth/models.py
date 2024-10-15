from sqlalchemy import  Column, Integer, String, DateTime , Numeric
from sqlalchemy.orm import relationship

from ...database import Base

class Authorize(Base):
    __tablename__ = "Authorize"

    ID = Column(Integer, primary_key=True)   
    AuthType = Column(String)
    ClientKey = Column(String)
    SecretKey = Column(String)
    Token = Column(String)
    ReToken = Column(String)
    IsUsed = Column(String)
    CreatedDate = Column(Numeric)
    UpdatedDate = Column(Numeric)
    ExpiryDate = Column(DateTime)



