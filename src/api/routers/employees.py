import fastapi
from fastapi import APIRouter

from src.api.views.employee import Employee as AWEmployee
from src.db.schemes.employee import Employee as DBEmployee
from src.db.session import session

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/{employee_id}")
async def employee(employee_id: int) -> AWEmployee:
    try:
        s = session()
    except:
        raise fastapi.HTTPException(500)

    tmp = s.get(DBEmployee, employee_id)

    if not tmp:
        raise fastapi.HTTPException(404)

    return AWEmployee(employee_id=tmp.EmployeeID, name=f"{tmp.LastName} {tmp.FirstName} {tmp.FatherName}")


@router.get("/")
@router.get("/list")
async def employees() -> list[AWEmployee]:
    s = session()
    return [AWEmployee(employee_id=row.EmployeeID, name=f"{row.LastName} {row.FirstName} {row.FatherName}") for row in s.query(DBEmployee).all()]
