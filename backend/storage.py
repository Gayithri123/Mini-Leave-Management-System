import os
import pandas as pd
from datetime import datetime
from dateutil.parser import isoparse

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EMP_FILE = os.path.join(DATA_DIR, "employees.xlsx")
LEAVE_FILE = os.path.join(DATA_DIR, "leaves.xlsx")

EMP_COLUMNS = ["id","name","email","department","joining_date","leave_balance"]
LEAVE_COLUMNS = ["id","employee_id","start_date","end_date","days","status","applied_at","reason"]

DEFAULT_ANNUAL_LEAVE = 24

def _ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(EMP_FILE):
        df = pd.DataFrame(columns=EMP_COLUMNS)
        df.to_excel(EMP_FILE, index=False)
    if not os.path.exists(LEAVE_FILE):
        df = pd.DataFrame(columns=LEAVE_COLUMNS)
        df.to_excel(LEAVE_FILE, index=False)

def _load_employees():
    _ensure_files()
    return pd.read_excel(EMP_FILE, dtype=str).fillna("")

def _load_leaves():
    _ensure_files()
    return pd.read_excel(LEAVE_FILE, dtype=str).fillna("")

def _save_employees(df):
    df.to_excel(EMP_FILE, index=False)

def _save_leaves(df):
    df.to_excel(LEAVE_FILE, index=False)

def _parse_date(s):
    try:
        return isoparse(s).date()
    except Exception:
        return None

def _next_employee_id():
    emps = _load_employees()
    if emps.empty:
        return "E001"
    nums = emps["id"].str.extract(r"E(\d+)")[0].dropna().astype(int)
    next_num = nums.max() + 1 if not nums.empty else 1
    return f"E{next_num:03d}"  # zero-padded until 999, then E1000+

def _next_leave_id():
    leaves = _load_leaves()
    if leaves.empty:
        return "L001"
    nums = leaves["id"].str.extract(r"L(\d+)")[0].dropna().astype(int)
    next_num = nums.max() + 1 if not nums.empty else 1
    return f"L{next_num:03d}"  # zero-padded until 999, then L1000+

def add_employee(emp_id, name, email, department, joining_date):
    if not emp_id:  # auto-generate if missing
        emp_id = _next_employee_id()

    emps = _load_employees()
    if (emps["id"] == emp_id).any():
        raise ValueError("Employee ID already exists")
    if (emps["email"].str.lower() == email.lower()).any():
        raise ValueError("Email already exists")

    jd = _parse_date(joining_date)
    if jd is None:
        raise ValueError("Invalid joining_date")

    new_row = {
        "id": emp_id,
        "name": name,
        "email": email,
        "department": department,
        "joining_date": jd.isoformat(),
        "leave_balance": str(DEFAULT_ANNUAL_LEAVE),
    }
    emps = pd.concat([emps, pd.DataFrame([new_row])], ignore_index=True)
    _save_employees(emps)
    return new_row

def get_employee(emp_id):
    emps = _load_employees()
    rows = emps[emps["id"] == emp_id]
    if rows.empty:
        return None
    return rows.iloc[0].to_dict()

def list_pending_leaves():
    leaves = _load_leaves()
    return leaves[leaves["status"] == "PENDING"].to_dict(orient="records")

def _calc_days(start_date, end_date):
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    if sd is None or ed is None:
        raise ValueError("Invalid dates")
    if ed < sd:
        raise ValueError("end_date before start_date")
    return (ed - sd).days + 1

def _has_overlap(emp_id, start_date, end_date):
    leaves = _load_leaves()
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    subset = leaves[(leaves["employee_id"] == emp_id) & (leaves["status"].isin(["PENDING","APPROVED"]))]
    for _, row in subset.iterrows():
        rsd = _parse_date(row["start_date"])
        red = _parse_date(row["end_date"])
        if not rsd or not red:
            continue
        if not (ed < rsd or sd > red):
            return True
    return False

def apply_leave(leave_id, employee_id, start_date, end_date, reason=""):
    if not leave_id:  # auto-generate if missing
        leave_id = _next_leave_id()

    emp = get_employee(employee_id)
    if not emp:
        raise ValueError("Employee not found")

    jd = _parse_date(emp["joining_date"])
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    if sd is None or ed is None:
        raise ValueError("Invalid dates")
    if ed < sd:
        raise ValueError("end_date before start_date")
    if sd < jd:
        raise ValueError("Cannot apply for leave before joining date")

    if _has_overlap(employee_id, start_date, end_date):
        raise ValueError("Overlapping leave request exists")

    days = _calc_days(start_date, end_date)
    balance = int(emp["leave_balance"]) if str(emp["leave_balance"]).strip() != "" else 0
    if days > balance:
        raise ValueError("Requested days exceed available balance")

    leaves = _load_leaves()
    if (leaves["id"] == leave_id).any():
        raise ValueError("Leave ID already exists")

    new_row = {
        "id": leave_id,
        "employee_id": employee_id,
        "start_date": sd.isoformat(),
        "end_date": ed.isoformat(),
        "days": str(days),
        "status": "PENDING",
        "applied_at": datetime.utcnow().isoformat(),
        "reason": reason or "",
    }
    leaves = pd.concat([leaves, pd.DataFrame([new_row])], ignore_index=True)
    _save_leaves(leaves)
    return new_row

def approve_leave(leave_id):
    leaves = _load_leaves()
    idx = leaves.index[leaves["id"] == leave_id].tolist()
    if not idx:
        raise ValueError("Leave not found")
    i = idx[0]
    if leaves.loc[i, "status"] != "PENDING":
        raise ValueError("Leave not in PENDING state")

    employee_id = leaves.loc[i, "employee_id"]
    days = int(leaves.loc[i, "days"])

    emp = get_employee(employee_id)
    if not emp:
        raise ValueError("Employee not found")

    balance = int(emp["leave_balance"]) if str(emp["leave_balance"]).strip() != "" else 0
    if days > balance:
        raise ValueError("Insufficient balance at approval time")

    emps = _load_employees()
    emp_idx = emps.index[emps["id"] == employee_id].tolist()[0]
    emps.loc[emp_idx, "leave_balance"] = str(balance - days)
    _save_employees(emps)

    leaves.loc[i, "status"] = "APPROVED"
    _save_leaves(leaves)
    return leaves.loc[i].to_dict()

def reject_leave(leave_id, reason=""):
    leaves = _load_leaves()
    idx = leaves.index[leaves["id"] == leave_id].tolist()
    if not idx:
        raise ValueError("Leave not found")
    i = idx[0]
    if leaves.loc[i, "status"] != "PENDING":
        raise ValueError("Leave not in PENDING state")

    leaves.loc[i, "status"] = "REJECTED"
    if reason:
        leaves.loc[i, "reason"] = reason
    _save_leaves(leaves)
    return leaves.loc[i].to_dict()

def get_balance(employee_id):
    emp = get_employee(employee_id)
    if not emp:
        raise ValueError("Employee not found")
    return int(emp["leave_balance"])

def list_employees():
    emps = _load_employees()
    return emps.to_dict(orient="records")
