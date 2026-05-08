from fastapi import Depends
from sqlmodel import Session

from .database import get_session
from .repositories.category_repository import CategoryRepository
from .repositories.ingredient_repository import IngredientRepository
from .repositories.product_repository import ProductRepository


class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.categorias = CategoryRepository(session)
        self.ingredientes = IngredientRepository(session)
        self.productos = ProductRepository(session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def refresh(self, entity: object) -> None:
        self.session.refresh(entity)


def get_uow(session: Session = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)
