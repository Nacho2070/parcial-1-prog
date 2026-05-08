from fastapi import HTTPException, status

from ..schemas.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from ..uow import UnitOfWork


class CategoryService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create(self, payload: CategoriaCreate) -> Categoria:
        if payload.parent_id is not None:
            parent = self.uow.categorias.get_by_id(payload.parent_id)
            if not parent or not parent.activo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria padre no encontrada")

        categoria = Categoria.model_validate(payload)
        self.uow.categorias.create(categoria)
        self.uow.commit()
        self.uow.refresh(categoria)
        return categoria

    def list_active(self, nombre: str | None = None) -> list[Categoria]:
        return self.uow.categorias.list_active(nombre)

    def get_active_by_id(self, categoria_id: int) -> Categoria:
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria or not categoria.activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
        return categoria

    def update(self, categoria_id: int, payload: CategoriaUpdate) -> Categoria:
        categoria = self.get_active_by_id(categoria_id)
        data = payload.model_dump(exclude_unset=True)

        if "parent_id" in data and data["parent_id"] is not None:
            if data["parent_id"] == categoria_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Una categoria no puede ser su propia padre")
            parent = self.uow.categorias.get_by_id(data["parent_id"])
            if not parent or not parent.activo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria padre no encontrada")

        for key, value in data.items():
            setattr(categoria, key, value)

        self.uow.commit()
        self.uow.refresh(categoria)
        return categoria

    def soft_delete(self, categoria_id: int) -> None:
        categoria = self.get_active_by_id(categoria_id)
        categoria.activo = False
        self.uow.commit()
