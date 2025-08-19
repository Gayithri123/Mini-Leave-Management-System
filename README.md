# 🗓 Leave Management System — FastAPI + React

This is my submission for a **Leave Management System** project.
The system allows employees to apply for leave, and managers/admins to approve/reject requests.
The project implements employee management, leave application, approval workflow, and balance tracking.

---

## ⚙️ Tech Stack

* 🔙 **Backend**: Python (FastAPI, pandas, openpyxl for Excel storage)
* ⚛️ **Frontend**: React (Vite)
* 📊 **Storage**: Excel files (`employees.xlsx`, `leaves.xlsx`) instead of SQL DB
* 🧪 **Testing**: Manual API testing via Postman / browser (can be extended to `pytest`)

---

## 📂 Project Structure

```
leave-mgmt-excel-fastapi-react/
├── backend/
│   ├── app.py                # FastAPI app (routes & API definitions)
│   ├── storage.py            # Excel persistence (employees, leaves)
│   ├── business_rules.py     # Leave policy rules (annual quota, date calc)
│   ├── data/
│   │   ├── employees.xlsx
│   │   └── leaves.xlsx
│   ├── requirements.txt
│   └── README_backend.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx           # React UI
│   │   └── main.jsx
│   ├── package.json
│   └── README_frontend.md
└── README.md                 # Root Readme (this file)
```

---

## 📑 Database Schema

For now, the data is stored in Excel files (`employees.xlsx`, `leaves.xlsx`).
Below are the equivalent **SQL-style schemas**, useful if migrating later:

### 🧍 Employee Table (`employees.xlsx` → `employees`)

| Column          | Type    | Constraints                  | Description                    |
| --------------- | ------- | ---------------------------- | ------------------------------ |
| `id`            | VARCHAR | PRIMARY KEY (format: `E001`) | Unique Employee ID             |
| `name`          | VARCHAR | NOT NULL                     | Full name of employee          |
| `email`         | VARCHAR | UNIQUE, NOT NULL             | Email address                  |
| `department`    | VARCHAR | NOT NULL                     | Department name                |
| `joining_date`  | DATE    | NOT NULL                     | Date of joining                |
| `leave_balance` | INT     | DEFAULT 24                   | Remaining annual leave balance |

---

### 📄 Leave Table (`leaves.xlsx` → `leaves`)

| Column        | Type     | Constraints                                           | Description                    |
| ------------- | -------- | ----------------------------------------------------- | ------------------------------ |
| `id`          | VARCHAR  | PRIMARY KEY (format: `L001`)                          | Unique Leave ID                |
| `employee_id` | VARCHAR  | FOREIGN KEY → `employees(id)`                         | ID of employee applying leave  |
| `start_date`  | DATE     | NOT NULL                                              | Leave start date               |
| `end_date`    | DATE     | NOT NULL                                              | Leave end date                 |
| `days`        | INT      | NOT NULL                                              | Number of leave days requested |
| `status`      | ENUM     | Default `PENDING` (`PENDING`, `APPROVED`, `REJECTED`) | Leave request status           |
| `applied_at`  | DATETIME | NOT NULL                                              | Timestamp when applied         |
| `reason`      | TEXT     | Optional                                              | Reason for leave               |

---

## 🧪 How to Run

### 🔧 Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Run the FastAPI app
uvicorn app:app --reload --port 8000
```

Server runs at: [http://localhost:8000](http://localhost:8000)
Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### ⚛️ Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Runs at: [http://localhost:5173](http://localhost:5173)

---

## ✅ Completed Features

### ✔️ Part 1: Employee Management

* Add new employee (ID auto-generated: `E001`, `E002`…)
* Validate email uniqueness
* Store joining date, department, and balance

### ✔️ Part 2: Leave Application

* Employee applies for leave
* Leave ID auto-generated: `L001`, `L002`…
* Validations:

  * Cannot apply before joining date
  * Cannot overlap with existing leaves
  * Cannot exceed available balance

### ✔️ Part 3: Leave Approval / Rejection

* Manager can **approve** or **reject** pending leave
* On approval → leave balance deducted
* On rejection → status updated with optional reason

### ✔️ Part 4: Balance Tracking

* API + UI to check current leave balance per employee
* Updated after each approval

---

## 🖥 UI Pages

* **Add Employee** → create new employee, view generated ID
* **Apply Leave** → apply leave using employee ID
* **Approvals** → manager dashboard to approve/reject pending leaves
* **Balance** → check leave balance for any employee

---

## 📈 Scaling Plan

* **Current MVP (Excel)**

  * Suitable for up to \~50 employees
  * Simple persistence in `.xlsx` files
  * Easy debugging & quick prototyping

* **When growing to \~500+ employees**

  * Replace Excel with a relational DB (Postgres/MySQL)
  * Use SQLAlchemy ORM for queries
  * Add indexing for faster lookups (employee ID, status)
  * Transactions for concurrent leave requests

* **Beyond 1000+ employees**

  * Add authentication & role-based access (Employee / Manager / Admin)
  * Introduce caching (Redis) for frequent reads (balances, pending leaves)
  * Containerize with Docker & deploy on cloud (Heroku/Render/Vercel + Postgres)
  * Consider microservices split (Employee Service, Leave Service) if scale demands

---
