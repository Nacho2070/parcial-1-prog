from sqlmodel import Session, select

from ..schemas.ingrediente import Ingrediente


class IngredientRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        self.session.add(ingrediente)
        return ingrediente

    def get_by_id(self, ingrediente_id: int) -> Ingrediente | None:
        return self.session.get(Ingrediente, ingrediente_id)

    def list_active(self, nombre: str | None = None) -> list[Ingrediente]:
        query = select(Ingrediente).where(Ingrediente.activo == True)
        if nombre:
            query = query.where(Ingrediente.nombre.contains(nombre))
        return self.session.exec(query).all()

    def list_active_by_ids(self, ingrediente_ids: list[int]) -> list[Ingrediente]:
        if not ingrediente_ids:
            return []
        query = select(Ingrediente).where(
            Ingrediente.id.in_(ingrediente_ids),
            Ingrediente.activo == True,
        )
        return self.session.exec(query).all()
