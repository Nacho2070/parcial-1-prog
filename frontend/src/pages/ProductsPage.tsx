import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useCreateProduct, useDeleteProduct, useProducts, useUpdateProduct } from '../hooks/useApiHooks'
import Modal from '../components/Modal'
import { useCategories, useIngredients } from '../hooks/useApiHooks'
import type { Product, ProductCreateInput, ProductUpdateInput } from '../types'

const ProductsPage: React.FC = () => {
  const { data: products, isLoading, error } = useProducts()
  const { data: categories } = useCategories()
  const { data: ingredients } = useIngredients()
  const createMutation = useCreateProduct()
  const updateMutation = useUpdateProduct()
  const deleteMutation = useDeleteProduct()

  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editing, setEditing] = useState<Product | null>(null)
  const [formData, setFormData] = useState<ProductCreateInput>({
    nombre: '',
    descripcion: '',
    precio: 0,
    categoria_id: 0,
    ingrediente_ids: [],
  })
  const [formError, setFormError] = useState<string | null>(null)

  const isFormValid = useMemo(
    () => formData.nombre.trim().length >= 2 && formData.precio > 0 && formData.categoria_id > 0,
    [formData],
  )

  const openCreate = () => {
    setEditing(null)
    setFormError(null)
    setFormData({ nombre: '', descripcion: '', precio: 0, categoria_id: 0, ingrediente_ids: [] })
    setIsModalOpen(true)
  }

  const openEdit = (product: Product) => {
    setEditing(product)
    setFormError(null)
    setFormData({
      nombre: product.nombre,
      descripcion: product.descripcion ?? '',
      precio: product.precio,
      categoria_id: product.categoria_id,
      ingrediente_ids: (product.ingredientes ?? []).map((i) => i.id),
    })
    setIsModalOpen(true)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)

    if (!isFormValid) {
      setFormError('Completa nombre (min 2), precio positivo y categoria.')
      return
    }

    if (editing) {
      const payload: ProductUpdateInput = {
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        precio: formData.precio,
        categoria_id: formData.categoria_id,
        ingrediente_ids: formData.ingrediente_ids,
      }
      updateMutation.mutate(
        { id: editing.id, data: payload },
        {
          onSuccess: () => {
            setIsModalOpen(false)
            setEditing(null)
          },
          onError: () => setFormError('No se pudo editar el producto.'),
        },
      )
      return
    }

    createMutation.mutate(formData, {
      onSuccess: () => {
        setIsModalOpen(false)
        setFormData({ nombre: '', descripcion: '', precio: 0, categoria_id: 0, ingrediente_ids: [] })
      },
      onError: () => setFormError('No se pudo crear el producto.'),
    })
  }

  const handleDelete = (id: number) => {
    if (!confirm('Eliminar producto?')) return
    deleteMutation.mutate(id)
  }

  if (isLoading) return <div className="p-8 text-slate-600">Cargando...</div>

  return (
    <div className="mx-auto max-w-4xl p-6">
      <div className="mb-5 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Listado de productos</h1>
        <button
          onClick={openCreate}
          className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Nuevo producto
        </button>
      </div>

      {error ? <p className="rounded bg-red-100 p-3 text-red-700">Error al cargar productos.</p> : null}

      <div className="overflow-hidden rounded-lg border border-slate-200">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-700">
            <tr>
              <th className="px-4 py-3">Nombre</th>
              <th className="px-4 py-3">Precio</th>
              <th className="px-4 py-3">Categoria</th>
              <th className="px-4 py-3">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {(products ?? []).map((product) => (
              <tr key={product.id} className="border-t border-slate-200">
                <td className="px-4 py-3">{product.nombre}</td>
                <td className="px-4 py-3">${product.precio.toFixed(2)}</td>
                <td className="px-4 py-3">{product.categoria?.nombre ?? '-'}</td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap gap-2">
                    <Link
                      to={`/detalle/${product.id}`}
                      className="rounded bg-slate-700 px-3 py-1 text-white hover:bg-slate-800"
                    >
                      Ver detalle
                    </Link>
                    <button
                      onClick={() => openEdit(product)}
                      className="rounded bg-indigo-600 px-3 py-1 text-white hover:bg-indigo-700"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(product.id)}
                      disabled={deleteMutation.isPending}
                      className="rounded bg-red-600 px-3 py-1 text-white disabled:bg-slate-400"
                    >
                      {deleteMutation.isPending ? '...' : 'Eliminar'}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <h2 className="text-xl font-semibold">{editing ? 'Editar producto' : 'Crear producto'}</h2>
          {formError ? <p className="rounded bg-red-100 p-2 text-sm text-red-700">{formError}</p> : null}
          <input
            type="text"
            value={formData.nombre}
            onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
            placeholder="Nombre"
            className={`w-full rounded border px-3 py-2 ${formData.nombre.trim().length < 2 ? 'border-red-400' : 'border-slate-300'}`}
          />
          <input
            type="text"
            value={formData.descripcion || ''}
            onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
            placeholder="Descripcion"
            className="w-full rounded border border-slate-300 px-3 py-2"
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="number"
              min="0"
              step="0.01"
              value={formData.precio}
              onChange={(e) => setFormData({ ...formData, precio: Number(e.target.value) })}
              placeholder="Precio"
              className={`w-full rounded border px-3 py-2 ${formData.precio <= 0 ? 'border-red-400' : 'border-slate-300'}`}
            />
            <select
              value={formData.categoria_id}
              onChange={(e) => setFormData({ ...formData, categoria_id: Number(e.target.value) })}
              className={`w-full rounded border px-3 py-2 ${formData.categoria_id <= 0 ? 'border-red-400' : 'border-slate-300'}`}
            >
              <option value={0}>Selecciona categoria</option>
              {(categories ?? []).map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.nombre}
                </option>
              ))}
            </select>
          </div>
          <div>
            <p className="mb-2 text-sm font-medium text-slate-700">Ingredientes</p>
            <p className="mb-2 text-xs text-slate-500">Marca los que apliquen (puedes elegir varios).</p>
            <div className="max-h-40 overflow-y-auto rounded border border-slate-300 bg-slate-50 p-2">
              {(ingredients ?? []).length === 0 ? (
                <p className="px-2 py-2 text-sm text-slate-500">No hay ingredientes cargados.</p>
              ) : (
                <ul className="space-y-1">
                  {(ingredients ?? []).map((ingredient) => {
                    const checked = formData.ingrediente_ids.includes(ingredient.id)
                    return (
                      <li key={ingredient.id}>
                        <label className="flex cursor-pointer items-center gap-2 rounded px-2 py-1.5 hover:bg-white">
                          <input
                            type="checkbox"
                            checked={checked}
                            onChange={() => {
                              setFormData((prev) => {
                                const set = new Set(prev.ingrediente_ids)
                                if (set.has(ingredient.id)) set.delete(ingredient.id)
                                else set.add(ingredient.id)
                                return { ...prev, ingrediente_ids: Array.from(set) }
                              })
                            }}
                            className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                          />
                          <span className="text-sm text-slate-800">{ingredient.nombre}</span>
                        </label>
                      </li>
                    )
                  })}
                </ul>
              )}
            </div>
            {formData.ingrediente_ids.length > 0 ? (
              <p className="mt-1 text-xs text-slate-500">
                Seleccionados: {formData.ingrediente_ids.length}
              </p>
            ) : null}
          </div>
          <button
            type="submit"
            disabled={!isFormValid || createMutation.isPending || updateMutation.isPending}
            className="w-full rounded bg-emerald-600 px-4 py-2 text-white disabled:bg-slate-400"
          >
            {createMutation.isPending || updateMutation.isPending ? 'Cargando...' : 'Guardar producto'}
          </button>
        </form>
      </Modal>
    </div>
  )
}

export default ProductsPage