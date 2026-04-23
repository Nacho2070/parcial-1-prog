from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .producto import Producto


class ProductoIngredienteLink(SQLModel, table=True):
    __tablename__ = "productoingrediente"

    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)


class IngredienteBase(SQLModel):
    nombre: str


class Ingrediente(IngredienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model=ProductoIngredienteLink,
    )


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = None


class IngredienteRead(IngredienteBase):
    id: int
    activo: bool