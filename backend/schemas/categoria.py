from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .producto import Producto


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, min_length=2, max_length=100)
    activo: bool = Field(default=True)

    productos: List["Producto"] = Relationship(back_populates="categoria")


class CategoriaCreate(SQLModel):
    nombre: str


class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = None


class CategoriaRead(SQLModel):
    id: int
    nombre: str
    activo: bool