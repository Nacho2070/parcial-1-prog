from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Ingrediente
from ..schemas import IngredienteCreate, IngredienteRead, IngredienteUpdate

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def create_ingrediente(payload: IngredienteCreate, session: Session = Depends(get_session)):
    ingrediente = Ingrediente.model_validate(payload)
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente


@router.get("/", response_model=list[IngredienteRead])
def list_ingredientes(
    session: Session = Depends(get_session),
    nombre: Annotated[Optional[str], Query(min_length=2, max_length=100)] = None,
):
    query = select(Ingrediente).where(Ingrediente.activo == True)
    if nombre:
        query = query.where(Ingrediente.nombre.contains(nombre))
    return session.exec(query).all()


@router.get("/{ingrediente_id}", response_model=IngredienteRead)
def get_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente or not ingrediente.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    return ingrediente


@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def update_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0)],
    payload: IngredienteUpdate,
    session: Session = Depends(get_session),
):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente or not ingrediente.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(ingrediente, key, value)

    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente


@router.delete("/{ingrediente_id}", response_model=dict[str, str])
def delete_ingrediente(
    ingrediente_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente or not ingrediente.activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    ingrediente.activo = False
    session.add(ingrediente)
    session.commit()
    return {"message": "Ingrediente desactivado"}