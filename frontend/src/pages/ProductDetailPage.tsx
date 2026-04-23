import React from 'react'
import { Link, useParams } from 'react-router-dom'

import { useProductDetail } from '../hooks/useProducts'

const ProductDetailPage: React.FC = () => {
  const { id } = useParams()
  const numericId = Number(id)
  const { data, isLoading, error } = useProductDetail(Number.isFinite(numericId) ? numericId : undefined)

  if (isLoading) return <div className="p-8">Cargando...</div>
  if (error) return <div className="p-8 text-red-700">Error al cargar el detalle.</div>
  if (!data) return <div className="p-8">No se encontro el producto.</div>

  return (
    <div className="mx-auto max-w-3xl p-6">
      <Link to="/" className="mb-4 inline-block rounded bg-slate-200 px-3 py-1 text-sm">
        Volver
      </Link>
      <h1 className="mb-2 text-2xl font-bold text-slate-800">{data.nombre}</h1>
      <p className="mb-1 text-slate-700">Precio: ${data.precio.toFixed(2)}</p>
      <p className="mb-3 text-slate-700">Categoria: {data.categoria?.nombre ?? '-'}</p>
      <p className="mb-3 text-slate-600">{data.descripcion || 'Sin descripcion'}</p>
      <div>
        <h2 className="mb-2 font-semibold">Ingredientes</h2>
        <ul className="list-disc pl-5 text-slate-700">
          {(data.ingredientes ?? []).map((ingredient) => (
            <li key={ingredient.id}>{ingredient.nombre}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default ProductDetailPage
