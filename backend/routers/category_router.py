from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Categoria
from ..schemas import CategoriaCreate, CategoriaRead, CategoriaUpdate

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def create_categoria(payload: CategoriaCreate, session: Session = Depends(get_session)):
    categoria = Categoria.model_validate(payload)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.get("/", response_model=list[CategoriaRead])
def list_categorias(
    session: Session = Depends(get_session),
    nombre: Annotated[Optional[str], Query(min_length=2, max_length=100)] = None,
):
    query = select(Categoria).where(Categoria.activo == True)
    if nombre:
        query = query.where(Categoria.nombre.contains(nombre))
    return session.exec(query).all()


@router.get("/{categoria_id}", response_model=CategoriaRead)
def get_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
):
    categoria = session.get(Categoria, categoria_id)
    if not categoria or not categoria.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaRead)
def update_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    payload: CategoriaUpdate,
    session: Session = Depends(get_session),
):
    categoria = session.get(Categoria, categoria_id)
    if not categoria or not categoria.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(categoria, key, value)

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", response_model=dict[str, str])
def delete_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
):
    categoria = session.get(Categoria, categoria_id)
    if not categoria or not categoria.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    categoria.activo = False
    session.add(categoria)
    session.commit()
    return {"message": "Categoria desactivada"}