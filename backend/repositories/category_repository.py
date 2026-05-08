from sqlmodel import Session, select

from ..schemas.categoria import Categoria


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, categoria: Categoria) -> Categoria:
        self.session.add(categoria)
        return categoria

    def get_by_id(self, categoria_id: int) -> Categoria | None:
        return self.session.get(Categoria, categoria_id)

    def list_active(self, nombre: str | None = None) -> list[Categoria]:
        query = select(Categoria).where(Categoria.activo == True)
        if nombre:
            query = query.where(Categoria.nombre.contains(nombre))
        return self.session.exec(query).all()
