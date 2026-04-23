from ..schemas.categoria import Categoria
from ..schemas.ingrediente import Ingrediente, ProductoIngredienteLink
from ..schemas.producto import Producto

# Keep backward-compatible name used by routers/code.
ProductoIngrediente = ProductoIngredienteLink
