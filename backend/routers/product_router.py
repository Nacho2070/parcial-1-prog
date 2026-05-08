from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query, status

from ..schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate
from ..services.product_service import ProductService
from ..uow import UnitOfWork, get_uow

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(
    payload: ProductoCreate,
    uow: UnitOfWork = Depends(get_uow),
    ):
    service = ProductService(uow)
    return service.create(payload)


@router.get("/", response_model=list[ProductoRead])
def list_productos(
    uow: UnitOfWork = Depends(get_uow),
    nombre: Annotated[Optional[str], Query(min_length=2, max_length=120)] = None,
    precio_min: Annotated[Optional[float], Query(gt=0)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 20,
):
    service = ProductService(uow)
    return service.list_active(nombre=nombre, precio_min=precio_min, skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(
    producto_id: Annotated[int, Path(gt=0)],
    uow: UnitOfWork = Depends(get_uow),
):
    service = ProductService(uow)
    return service.get_active_by_id(producto_id)


@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(
    producto_id: Annotated[int, Path(gt=0)],
    payload: ProductoUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = ProductService(uow)
    return service.update(producto_id, payload)


@router.delete("/{producto_id}", response_model=dict[str, str])
def delete_producto(
    producto_id: Annotated[int, Path(gt=0)],
    uow: UnitOfWork = Depends(get_uow),
):
    service = ProductService(uow)
    service.soft_delete(producto_id)
    return {"message": "Producto desactivado"}