from pydantic import BaseModel

class Employee(BaseModel):
    employee_id: int
    name: str
