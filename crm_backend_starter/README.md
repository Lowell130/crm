# CRM Backend (FastAPI + Beanie/MongoDB)

Starter backend for the CRM project with JWT auth, customer CRUD, search & filters, email/WhatsApp stubs, and export endpoints.

## Quickstart

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Then edit .env
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Mongo
Use a MongoDB Atlas URI or run local:
```bash
docker run -d --name mongo -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo:7
# then set MONGO_URI="mongodb://admin:admin@localhost:27017/?authSource=admin"
```
