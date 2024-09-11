# Installation

```bash
pip install requirements.txt
cd frontend && yarn install
openssl rand -hex 32 > backend/.env
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
