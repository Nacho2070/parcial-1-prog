from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db_and_tables
from .routers.category_router import router as category_router
from .routers.ingredient_router import router as ingredient_router
from .routers.product_router import router as product_router

app = FastAPI(title="Parcial CRUD API", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev server (Vite on 5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(category_router)
app.include_router(ingredient_router)
app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "API de productos lista"}