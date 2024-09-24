# Installation

```bash
pip install requirements.txt
# Run the migrations for the database and seed it with sample data
alembic -x seed_data=true upgrade head
cd frontend && yarn install
cd ..
echo "BACKEND_URL=http://localhost:8000" > frontend/.env
echo "SECRET_KEY=$(openssl rand -hex 32)" > backend/.env
```

# Running backend and frontend

### Backend

```bash
uvicorn backend.main:app --reload
```

### Frontend

```bash
yarn dev --open
```

# Backend Documentation

- Start the backend server and go to 'http://localhost:8000/docs/' to find in depth documentation about possible errors, expected input and return objects

## Updating the backend database

```bash
# create a new revision
alembic revision --autogenerate -m "your message here"
# apply the changes to the database
alembic upgrade head
```

## Backend Database Deployment

Make sure to set the database URL correctly:

```bash
export DATABASE_URL=postgresql://username:password@hostname:port/dbname
```
