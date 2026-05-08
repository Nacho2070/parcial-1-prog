from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .producto import Producto


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, min_length=2, max_length=100)
    activo: bool = Field(default=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    productos: List["Producto"] = Relationship(back_populates="categoria")
    parent: Optional["Categoria"] = Relationship(
        back_populates="subcategorias",
        sa_relationship_kwargs={"remote_side": "Categoria.id"},
    )
    subcategorias: List["Categoria"] = Relationship(back_populates="parent")


class CategoriaCreate(SQLModel):
    nombre: str
    parent_id: Optional[int] = None


class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = None
    parent_id: Optional[int] = None


class CategoriaRead(SQLModel):
    id: int
    nombre: str
    activo: bool
    parent_id: Optional[int] = None