# Parcial 1 - FastAPI + React

Proyecto fullstack para gestionar `productos`, `categorias` e `ingredientes` con FastAPI + SQLModel en backend y React + TypeScript + TanStack Query en frontend.
## Link video: https://drive.google.com/drive/u/0/folders/1nhBfNedY2tAo9zx-1bJziTU8cQSZ8HK6
## Arquitectura General

- **Backend (`backend/`)**: API REST modular por `routers`, `models` y `schemas`.
- **Frontend (`frontend/`)**: SPA con React Router, estado servidor con TanStack Query y estilos con Tailwind CSS 4.
- **Base de datos**: PostgreSQL (configurable con `DATABASE_URL`).

## Backend (FastAPI + SQLModel)

### Modelado implementado

- `Categoria` -> `Producto`: relacion **1:N** usando `categoria_id` como llave foranea.
- `Producto` <-> `Ingrediente`: relacion **N:N** usando tabla intermedia `ProductoIngrediente`.
- Relaciones declaradas con `Relationship` + `back_populates`.

### Seguridad y validaciones

- Todos los endpoints usan `response_model`.
- Se usa `Annotated` con `Query` y `Path` para validar:
  - nombres con longitud minima
  - precios positivos
  - IDs mayores que 0

### Endpoints principales

- `GET/POST /categorias`
- `GET/PUT/DELETE /categorias/{categoria_id}`
- `GET/POST /ingredientes`
- `GET/PUT/DELETE /ingredientes/{ingrediente_id}`
- `GET/POST /productos`
- `GET/PUT/DELETE /productos/{producto_id}`

## Frontend (React + TS + Tailwind)

- Interfaces tipadas para `Product`, `Category` e `Ingredient`.
- `useQuery` para listar productos.
- `useMutation` para crear producto.
- `invalidateQueries` en `onSuccess` para refrescar la lista automaticamente.
- Modal con formulario en Tailwind CSS y estados visuales de error/carga.
- Rutas:
  - `/` listado de productos
  - `/detalle/:id` detalle dinamico por ID

### useParams + useQuery en ruta dinamica

En `ProductDetailPage` se usa:

1. `const { id } = useParams()` para capturar el parametro de URL.
2. Se convierte a numero (`Number(id)`).
3. Ese valor se pasa al hook `useProductDetail(id)` que ejecuta un `useQuery` contra `/productos/{id}`.
4. Si no hay ID valido, el query no se ejecuta (`enabled: !!id`).

## Ejecucion local

## 1) Backend con entorno virtual `.venv`

Desde la raiz del proyecto:

```bash
python -m venv .venv
```

Activar entorno:

- **Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -e ./backend
```

Configurar variable de entorno:

```powershell
$env:DATABASE_URL="postgresql+psycopg2://postgres:root@localhost:5432/parcial1"
```

Levantar servidor FastAPI:

```bash
uvicorn backend.main:app --reload --port 8000
```

## 2) Frontend con Vite

```bash
cd frontend
npm install
npm run dev
```

Frontend disponible en `http://localhost:5173` y API en `http://localhost:8000`.

## Scripts de Video (Evaluacion)

### Guion Backend (5 min)

1. Presento la arquitectura modular: separacion en `models`, `schemas` y `routers`.
2. Explico la relacion 1:N: una `Categoria` puede tener muchos `Producto`, por eso `Producto` tiene `categoria_id`.
3. Explico la relacion N:N: un `Producto` puede tener varios `Ingrediente` y un ingrediente puede pertenecer a varios productos. Para eso se usa `ProductoIngrediente` como tabla puente.
4. Muestro que SQLModel permite declarar estas asociaciones con `Relationship(back_populates=...)`.
5. Justifico `response_model`: evita exponer campos internos y garantiza respuesta consistente.
6. Detallo validaciones con `Annotated`:
   - `Query(min_length=2)` para filtros por nombre.
   - `Query(gt=0)` para precios.
   - `Path(gt=0)` para IDs.
7. Cierro con beneficios: integridad de datos, API mas segura y contrato claro para frontend.

### Guion Frontend (5 min)

1. Introduzco React Query como solucion de estado servidor.
2. Comparo con `useEffect + useState`:
   - Con `useEffect` debo manejar manualmente cache, loading, error y re-fetch.
   - Con TanStack Query eso viene resuelto en hooks reutilizables.
3. Muestro `useQuery` para listado de productos y estados `isLoading/error`.
4. Muestro `useMutation` para crear productos.
5. Explico `onSuccess + invalidateQueries(['productos'])`: evita inconsistencias y sincroniza vista con backend.
6. Explico modal con Tailwind:
   - feedback visual de campos invalidos
   - boton deshabilitado si datos no cumplen reglas
   - estado `Cargando...` durante mutacion
7. Cierro con el valor tecnico: menor codigo repetido, mejor UX y escalabilidad.

### Desafios tecnicos realistas (y solucion)

- **Relacion N:N no persistia ingredientes** -> se resolvio usando `link_model=ProductoIngrediente` y asignando lista de entidades cargadas desde DB.
- **Datos desactualizados despues de crear** -> se resolvio con `invalidateQueries` en `onSuccess`.
- **Errores por endpoints no alineados backend/frontend** -> se unifico convencion en espanol (`/productos`, `/categorias`, `/ingredientes`).
- **Formulario permitia precio 0** -> validacion dual: frontend (estado visual) + backend (`Query(gt=0)` y campo `Field(gt=0)`).
- **Rutas con recarga completa** -> se reemplazo `<a>` por `Link` de `react-router-dom`.
- **Conexion rigida a Postgres** -> se parametrizo via `DATABASE_URL` para facilitar despliegue y pruebas.
