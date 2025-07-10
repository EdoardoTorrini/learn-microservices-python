from pydantic import BaseModel


class PrimeDescriptor(BaseModel):
    lower_bound: int
    upper_bound: int
    email: str