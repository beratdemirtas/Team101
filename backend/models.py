from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    risk_profile: str = "Orta"
    balance: float = 10000.0
