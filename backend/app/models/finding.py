from sqlalchemy import Column, Integer, String
from app.database import Base

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, index=True)
    severity = Column(String, index=True)
    asset = Column(String)
    tool = Column(String)
    status = Column(String, default="Open")
