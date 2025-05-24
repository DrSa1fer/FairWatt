# from fastapi import APIRouter
#
# from src.api.views.employee import Employee as AWEmployee
# from src.db.schemes.employee import X as DBEmployee
# from src.db.session import session
#
# router = APIRouter()
#
# @router.get("/consumption/{employee_id}")
# async def consumption(consumption_id: int, is_day : bool = False) -> AWEmployee:
#     s = session()
#     row = s.get(DBEmployee, (consumption_id,))
#     return AWEmployee(employee_id=row.EmployeeID, name=f"{row.LastName} {row.FirstName} {row.FatherName}")
#
#
# @router.get("/employees")
# @router.get("/employee/list")
# async def employees() -> list[AWEmployee]:
#     s = session()
#     return [AWEmployee(employee_id=row.EmployeeID, name=f"{row.LastName} {row.FirstName} {row.FatherName}") for row in s.query(DBEmployee).all()]
