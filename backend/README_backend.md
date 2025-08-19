# Backend (FastAPI + Excel via pandas)

## Quickstart
```bash
cd backend
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## API Endpoints
- `GET /health`
- `POST /employees`
- `GET /employees`
- `POST /leaves/apply`
- `POST /leaves/approve`
- `POST /leaves/reject`
- `GET /employees/{emp_id}/balance`
- `GET /leaves/pending`

Data is stored in `backend/data/employees.xlsx` and `backend/data/leaves.xlsx`.
