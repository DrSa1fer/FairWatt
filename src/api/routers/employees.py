from fastapi import APIRouter

from src.api.views.employee import Employee as AWEmployee
from src.db.schemes.employee import Employee as DBEmployee
from src.db.session import session

router = APIRouter(tags=["employees"])

@router.get("/employees/{employee_id}")
async def employee(employee_id: int) -> AWEmployee:
    s = session()
    row = s.get(DBEmployee, (employee_id,))
    return AWEmployee(employee_id=row.EmployeeID, name=f"{row.LastName} {row.FirstName} {row.FatherName}")


@router.get("/employees")
async def employees() -> list[AWEmployee]:
    s = session()
    return [AWEmployee(employee_id=row.EmployeeID, name=f"{row.LastName} {row.FirstName} {row.FatherName}") for row in s.query(DBEmployee).all()]
