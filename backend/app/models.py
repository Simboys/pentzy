from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, index=True)
    severity = Column(String)
    asset = Column(String)
    tool = Column(String)
    status = Column(String, default="Open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
