# CHECKLIST - Parcial 1

## Bloque 1: Arquitectura DB y Backend

- [x] Estructura modular en backend (`routers`, `models`, `schemas`)
- [x] Modelos SQLModel: `Categoria`, `Producto`, `Ingrediente`
- [x] Relacion 1:N entre `Categoria` y `Producto`
- [x] Relacion N:N entre `Producto` e `Ingrediente` con `ProductoIngrediente`
- [x] Uso de `Relationship` y `back_populates`
- [x] Validaciones con `Annotated`, `Query` y `Path`
- [x] `response_model` aplicado en endpoints
- [x] Conexion a PostgreSQL configurable por `DATABASE_URL`
- [x] CRUD basico implementado para los 3 modulos

## Bloque 2: Frontend y Estado

- [x] Interfaces TypeScript alineadas con backend
- [x] `useQuery` para listar productos
- [x] `useMutation` para crear producto
- [x] `invalidateQueries` dentro de `onSuccess`
- [x] Modal de formulario con Tailwind CSS 4
- [x] Estados visuales: `Cargando...` y `Error`

## Bloque 3: Navegacion y Rutas Dinamicas

- [x] Ruta principal de listado de productos (`/`)
- [x] Ruta dinamica de detalle (`/detalle/:id`)
- [x] Uso de `useParams` para capturar ID
- [x] Uso del ID en `useQuery` para traer detalle

## Bloque 4: Guion de video

- [x] Guion backend de 5 minutos (N:N + `Annotated`)
- [x] Guion frontend de 5 minutos (TanStack Query vs `useEffect`)
- [x] Lista de desafios tecnicos realistas con soluciones

## Bloque 5: Documentacion final

- [x] README profesional generado
- [x] Instrucciones para crear/usar `.venv`
- [x] Instrucciones para correr FastAPI
- [x] Instrucciones para correr Vite
