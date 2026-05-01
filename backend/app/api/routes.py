from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth import authenticate_user, create_access_token, get_current_user

router = APIRouter()

# ============ MODÈLES PYDANTIC ============
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

# ============ BASE DE DONNÉES TEMPORAIRE ============
items_db = [
    {"id": 1, "name": "Item 1", "description": "Description 1"},
    {"id": 2, "name": "Item 2", "description": "Description 2"}
]

# ============ ROUTES D'AUTHENTIFICATION ============
@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name}
    }

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "full_name": current_user.full_name}

# ============ ROUTES EXISTANTES ============
@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend FastAPI is running"}

@router.get("/data", response_model=List[Item])
async def get_data(current_user: User = Depends(get_current_user)):
    """Récupère tous les items (protégé par auth)"""
    return items_db

@router.get("/data/{item_id}", response_model=Item)
async def get_item(item_id: int, current_user: User = Depends(get_current_user)):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/data", response_model=Item)
async def create_item(item: ItemCreate, current_user: User = Depends(get_current_user)):
    new_id = max([i["id"] for i in items_db]) + 1 if items_db else 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return new_item

@router.put("/data/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate, current_user: User = Depends(get_current_user)):
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            items_db[i] = {"id": item_id, **item.dict()}
            return items_db[i]
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/data/{item_id}")
async def delete_item(item_id: int, current_user: User = Depends(get_current_user)):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")