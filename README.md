## decor-castle-vendor-manager

### FastAPI development setup

**1. Create and activate virtual environment (once per shell)**

```bash
cd /home/hdz666/Desktop/decor-castle/decor-castle-vendor-manager
python3 -m venv .venv
. .venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure database environment variables**

Edit `.env` (created in the project root) to match your local Postgres setup. Example:

```env
DB_HOST=127.0.0.1
DB_PORT=5433
DB_USER=newuser
DB_PASSWORD=SuperStrongPass123!
DB_NAME=vendor_manager
```

**4. Run Alembic migrations**

Initialize a first migration (this will create an empty revision you can edit later):

```bash
alembic revision -m "initial schema"
alembic upgrade head
```

**5. Run the FastAPI app with Uvicorn (auto-reload for development)**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and the interactive docs at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
