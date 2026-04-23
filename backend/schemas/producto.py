from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .categoria import Categoria, CategoriaRead
from .ingrediente import Ingrediente, IngredienteRead, ProductoIngredienteLink


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    precio: float = Field(gt=0)
    activo: bool = Field(default=True)
    categoria_id: int = Field(foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="productos")
    ingredientes: List[Ingrediente] = Relationship(
        back_populates="productos",
        link_model=ProductoIngredienteLink,
    )


class ProductoCreate(SQLModel):
    nombre: str = Field(..., min_length=3, max_length=120)
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    categoria_id: int = Field(..., gt=0)
    ingrediente_ids: list[int] = Field(default_factory=list)


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria_id: Optional[int] = None
    ingrediente_ids: Optional[list[int]] = None


class ProductoRead(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    activo: bool
    categoria_id: int
    categoria: Optional[CategoriaRead] = None
    ingredientes: list[IngredienteRead] = Field(default_factory=list)