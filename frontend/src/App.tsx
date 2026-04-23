import { Link, Route, Routes } from 'react-router-dom'
import CategoriesPage from './pages/CategoriesPage'
import IngredientsPage from './pages/IngredientsPage'
import ProductDetailPage from './pages/ProductDetailPage'
import ProductsPage from './pages/ProductsPage'

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="flex gap-3 border-b border-slate-200 bg-white p-4">
        <Link to="/" className="rounded bg-slate-900 px-3 py-1 text-white">
          Productos
        </Link>
        <Link to="/categorias" className="rounded bg-slate-200 px-3 py-1 text-slate-700">
          Categorias
        </Link>
        <Link to="/ingredientes" className="rounded bg-slate-200 px-3 py-1 text-slate-700">
          Ingredientes
        </Link>
      </nav>
      <Routes>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/detalle/:id" element={<ProductDetailPage />} />
        <Route path="/categorias" element={<CategoriesPage />} />
        <Route path="/ingredientes" element={<IngredientsPage />} />
      </Routes>
    </div>
  )
}

export default App