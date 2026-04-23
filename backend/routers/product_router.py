from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from ..database import get_session
from ..models import Categoria, Ingrediente, Producto
from ..schemas import ProductoCreate, ProductoRead, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(
    payload: ProductoCreate, 
    session: Session = Depends(get_session),
    ):
    categoria = session.get(Categoria, payload.categoria_id)
    if not categoria or not categoria.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")

    producto = Producto(
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        precio=payload.precio,
        categoria_id=payload.categoria_id,
    )

    if payload.ingrediente_ids:
        ingredientes = session.exec(
            select(Ingrediente).where(
                Ingrediente.id.in_(payload.ingrediente_ids), Ingrediente.activo == True
            )
        ).all()
        producto.ingredientes = ingredientes

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.get("/", response_model=list[ProductoRead])
def list_productos(
    session: Session = Depends(get_session),
    nombre: Annotated[Optional[str], Query(min_length=2, max_length=120)] = None,
    precio_min: Annotated[Optional[float], Query(gt=0)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 20,
):
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
    return session.exec(query).all()


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(
    producto_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
):
    producto = session.exec(
        select(Producto)
        .where(Producto.id == producto_id, Producto.activo == True)
        .options(selectinload(Producto.categoria), selectinload(Producto.ingredientes))
    ).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(
    producto_id: Annotated[int, Path(gt=0)],
    payload: ProductoUpdate,
    session: Session = Depends(get_session),
):
    producto = session.get(Producto, producto_id)
    if not producto or not producto.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    data = payload.model_dump(exclude_unset=True, exclude={"ingrediente_ids"})
    for key, value in data.items():
        setattr(producto, key, value)

    if payload.ingrediente_ids is not None:
        ingredientes = session.exec(
            select(Ingrediente).where(
                Ingrediente.id.in_(payload.ingrediente_ids), Ingrediente.activo == True
            )
        ).all()
        producto.ingredientes = ingredientes

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/{producto_id}", response_model=dict[str, str])
def delete_producto(
    producto_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
):
    producto = session.get(Producto, producto_id)
    if not producto or not producto.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    producto.activo = False
    session.add(producto)
    session.commit()
    return {"message": "Producto desactivado"}