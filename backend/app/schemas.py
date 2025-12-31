from pydantic import BaseModel

class FindingCreate(BaseModel):
    cve_id: str
    severity: str
    asset: str
    tool: str

class FindingOut(FindingCreate):
    id: int
    status: str

    class Config:
    	from_attributes = True

class FindingUpdateStatus(BaseModel):
    status: str
