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
### Item Configs 
- `GET /api/item_configs/` - Get all item configs
- `POST /api/item_configs/` - Create a new item config using this format:
```json
{
    "triangle_size": 10,
    "triangle_color": "#ffffff",
    "circle_size": 10,
    "circle_color": "#ffffff",
    "time_visible_ms": 1000
}
```
- `GET /api/item_configs/{item_config_id}` - Get a specific item config
- `PUT /api/item_configs/{item_config_id}` - Update a specific item config using the same format as POST
- `DELETE /api/item_configs/{item_config_id}` - Delete a specific item config