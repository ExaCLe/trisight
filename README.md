# Installation
```bash
pip install 'fastapi[all]' sqlalchemy
cd frontend && yarn install
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