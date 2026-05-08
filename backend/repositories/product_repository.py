from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from ..schemas.producto import Producto


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, producto: Producto) -> Producto:
        self.session.add(producto)
        return producto

    def get_by_id(self, producto_id: int) -> Producto | None:
        return self.session.get(Producto, producto_id)

    def get_active_with_relations(self, producto_id: int) -> Producto | None:
        query = (
            select(Producto)
            .where(Producto.id == producto_id, Producto.activo == True)
            .options(selectinload(Producto.categoria), selectinload(Producto.ingredientes))
        )
        return self.session.exec(query).first()

    def list_active_with_relations(
        self,
        nombre: str | None = None,
        precio_min: float | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Producto]:
        query = (
            select(Producto)
            .where(Producto.activo == True)
            .options(selectinload(Producto.categoria), selectinload(Producto.ingredientes))
            .offset(skip)
            .limit(limit)
        )
        if nombre:
            query = query.where(Producto.nombre.contains(nombre))
        if precio_min is not None:
            query = query.where(Producto.precio >= precio_min)
        return self.session.exec(query).all()
