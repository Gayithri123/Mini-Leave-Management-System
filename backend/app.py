from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from storage import add_employee, apply_leave, approve_leave, reject_leave, get_balance, list_pending_leaves, list_employees
from storage import _next_employee_id, _next_leave_id

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5173")

app = FastAPI(title="Mini Leave Management System (Excel-backed)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[BASE_URL, "http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmployeeIn(BaseModel):
    id: Optional[str] = None   # auto-generated if not given
    name: str
    email: EmailStr
    department: str
    joining_date: str  # ISO date

class LeaveApplyIn(BaseModel):
    id: Optional[str] = None   # auto-generated if not given
    employee_id: str
    start_date: str
    end_date: str
    reason: Optional[str] = ""

class LeaveDecisionIn(BaseModel):
    id: str
    reason: Optional[str] = ""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/employees")
def create_employee(emp: EmployeeIn):
    try:
        row = add_employee(emp.id, emp.name, emp.email, emp.department, emp.joining_date)
        return {"message": "Employee created", "employee": row}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/employees")
def api_list_employees():
    return {"employees": list_employees()}

@app.post("/leaves/apply")
def api_apply_leave(body: LeaveApplyIn):
    try:
        row = apply_leave(body.id, body.employee_id, body.start_date, body.end_date, body.reason or "")
        return {"message": "Leave applied", "leave": row}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/leaves/approve")
def api_approve_leave(body: LeaveDecisionIn):
    try:
        row = approve_leave(body.id)
        return {"message": "Leave approved", "leave": row}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/leaves/reject")
def api_reject_leave(body: LeaveDecisionIn):
    try:
        row = reject_leave(body.id, body.reason or "")
        return {"message": "Leave rejected", "leave": row}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/employees/{emp_id}/balance")
def api_get_balance(emp_id: str):
    try:
        bal = get_balance(emp_id)
        return {"employee_id": emp_id, "balance": bal}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/leaves/pending")
def api_pending_leaves():
    return {"pending": list_pending_leaves()}

@app.get("/employees/next-id")
def api_next_emp_id():
    return {"next_id": _next_employee_id()}

@app.get("/leaves/next-id")
def api_next_leave_id():
    return {"next_id": _next_leave_id()}