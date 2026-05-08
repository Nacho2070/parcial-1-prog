from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query, status

from ..schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from ..services.category_service import CategoryService
from ..uow import UnitOfWork, get_uow

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def create_categoria(payload: CategoriaCreate, uow: UnitOfWork = Depends(get_uow)):
    service = CategoryService(uow)
    return service.create(payload)


@router.get("/", response_model=list[CategoriaRead])
def list_categorias(
    uow: UnitOfWork = Depends(get_uow),
    nombre: Annotated[Optional[str], Query(min_length=2, max_length=100)] = None,
):
    service = CategoryService(uow)
    return service.list_active(nombre)


@router.get("/{categoria_id}", response_model=CategoriaRead)
def get_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    uow: UnitOfWork = Depends(get_uow),
):
    service = CategoryService(uow)
    return service.get_active_by_id(categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaRead)
def update_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    payload: CategoriaUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = CategoryService(uow)
    return service.update(categoria_id, payload)


@router.delete("/{categoria_id}", response_model=dict[str, str])
def delete_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    uow: UnitOfWork = Depends(get_uow),
):
    service = CategoryService(uow)
    service.soft_delete(categoria_id)
    return {"message": "Categoria desactivada"}