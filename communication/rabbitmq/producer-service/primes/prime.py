from pydantic import BaseModel

class Prime(BaseModel):
    lower_bound: int
    upper_bound: int
    email: str