from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query, status

from ..schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate
from ..services.ingredient_service import IngredientService
from ..uow import UnitOfWork, get_uow

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def create_ingrediente(payload: IngredienteCreate, uow: UnitOfWork = Depends(get_uow)):
    service = IngredientService(uow)
    return service.create(payload)


@router.get("/", response_model=list[IngredienteRead])
def list_ingredientes(
    uow: UnitOfWork = Depends(get_uow),
    nombre: Annotated[Optional[str], Query(min_length=2, max_length=100)] = None,
):
    service = IngredientService(uow)
    return service.list_active(nombre)


@router.get("/{ingrediente_id}", response_model=IngredienteRead)
def get_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0)],
    uow: UnitOfWork = Depends(get_uow),
):
    service = IngredientService(uow)
    return service.get_active_by_id(ingrediente_id)


@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def update_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0)],
    payload: IngredienteUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = IngredientService(uow)
    return service.update(ingrediente_id, payload)


@router.delete("/{ingrediente_id}", response_model=dict[str, str])
def delete_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0)],
    uow: UnitOfWork = Depends(get_uow),
):
    service = IngredientService(uow)
    service.soft_delete(ingrediente_id)
    return {"message": "Ingrediente desactivado"}