from fastapi import HTTPException, status

from ..schemas.ingrediente import Ingrediente, IngredienteCreate, IngredienteUpdate
from ..uow import UnitOfWork


class IngredientService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create(self, payload: IngredienteCreate) -> Ingrediente:
        ingrediente = Ingrediente.model_validate(payload)
        self.uow.ingredientes.create(ingrediente)
        self.uow.commit()
        self.uow.refresh(ingrediente)
        return ingrediente

    def list_active(self, nombre: str | None = None) -> list[Ingrediente]:
        return self.uow.ingredientes.list_active(nombre)

    def get_active_by_id(self, ingrediente_id: int) -> Ingrediente:
        ingrediente = self.uow.ingredientes.get_by_id(ingrediente_id)
        if not ingrediente or not ingrediente.activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
        return ingrediente

    def update(self, ingrediente_id: int, payload: IngredienteUpdate) -> Ingrediente:
        ingrediente = self.get_active_by_id(ingrediente_id)
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(ingrediente, key, value)
        self.uow.commit()
        self.uow.refresh(ingrediente)
        return ingrediente

    def soft_delete(self, ingrediente_id: int) -> None:
        ingrediente = self.get_active_by_id(ingrediente_id)
        ingrediente.activo = False
        self.uow.commit()
