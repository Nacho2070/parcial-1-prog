from fastapi import HTTPException, status

from ..schemas.producto import Producto, ProductoCreate, ProductoUpdate
from ..uow import UnitOfWork


class ProductService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create(self, payload: ProductoCreate) -> Producto:
        categoria = self.uow.categorias.get_by_id(payload.categoria_id)
        if not categoria or not categoria.activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")

        producto = Producto(
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            precio=payload.precio,
            categoria_id=payload.categoria_id,
        )
        if payload.ingrediente_ids:
            producto.ingredientes = self.uow.ingredientes.list_active_by_ids(payload.ingrediente_ids)

        self.uow.productos.create(producto)
        self.uow.commit()
        self.uow.refresh(producto)
        return self.get_active_by_id(producto.id)

    def list_active(
        self,
        nombre: str | None = None,
        precio_min: float | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Producto]:
        return self.uow.productos.list_active_with_relations(
            nombre=nombre,
            precio_min=precio_min,
            skip=skip,
            limit=limit,
        )

    def get_active_by_id(self, producto_id: int | None) -> Producto:
        if producto_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        producto = self.uow.productos.get_active_with_relations(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return producto

    def update(self, producto_id: int, payload: ProductoUpdate) -> Producto:
        producto = self.uow.productos.get_by_id(producto_id)
        if not producto or not producto.activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        data = payload.model_dump(exclude_unset=True, exclude={"ingrediente_ids"})
        if "categoria_id" in data:
            categoria = self.uow.categorias.get_by_id(data["categoria_id"])
            if not categoria or not categoria.activo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")

        for key, value in data.items():
            setattr(producto, key, value)

        if payload.ingrediente_ids is not None:
            producto.ingredientes = self.uow.ingredientes.list_active_by_ids(payload.ingrediente_ids)

        self.uow.commit()
        self.uow.refresh(producto)
        return self.get_active_by_id(producto.id)

    def soft_delete(self, producto_id: int) -> None:
        producto = self.uow.productos.get_by_id(producto_id)
        if not producto or not producto.activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        producto.activo = False
        self.uow.commit()
