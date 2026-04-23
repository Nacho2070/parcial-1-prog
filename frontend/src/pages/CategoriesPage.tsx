import React, { useMemo, useState } from 'react'
import Modal from '../components/Modal'
import { useCategories, useCreateCategory, useDeleteCategory, useUpdateCategory } from '../hooks/useCategories'
import type { Category } from '../types'

const CategoriesPage: React.FC = () => {
  const { data: categories, isLoading, error } = useCategories()
  const createMutation = useCreateCategory()
  const updateMutation = useUpdateCategory()
  const deleteMutation = useDeleteCategory()

  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editing, setEditing] = useState<Category | null>(null)
  const [nombre, setNombre] = useState('')
  const [formError, setFormError] = useState<string | null>(null)

  const isValid = useMemo(() => nombre.trim().length >= 2, [nombre])

  const openCreate = () => {
    setEditing(null)
    setNombre('')
    setFormError(null)
    setIsModalOpen(true)
  }

  const openEdit = (category: Category) => {
    setEditing(category)
    setNombre(category.nombre)
    setFormError(null)
    setIsModalOpen(true)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)
    if (!isValid) {
      setFormError('El nombre debe tener al menos 2 caracteres.')
      return
    }

    const payload = { nombre: nombre.trim() }
    if (editing) {
      updateMutation.mutate(
        { id: editing.id, data: payload },
        {
          onSuccess: () => setIsModalOpen(false),
          onError: () => setFormError('No se pudo editar la categoria.'),
        },
      )
      return
    }

    createMutation.mutate(payload, {
      onSuccess: () => setIsModalOpen(false),
      onError: () => setFormError('No se pudo crear la categoria.'),
    })
  }

  const handleDelete = (id: number) => {
    if (!confirm('Eliminar categoria?')) return
    deleteMutation.mutate(id)
  }

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="mx-auto max-w-3xl p-6">
      <div className="mb-5 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Categorias</h1>
        <button onClick={openCreate} className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Nueva categoria
        </button>
      </div>

      {error ? <p className="rounded bg-red-100 p-3 text-red-700">Error al cargar categorias.</p> : null}

      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-700">
            <tr>
              <th className="px-4 py-3">Nombre</th>
              <th className="px-4 py-3">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {(categories ?? []).map((category) => (
              <tr key={category.id} className="border-t border-slate-200">
                <td className="px-4 py-3">{category.nombre}</td>
                <td className="px-4 py-3">
                  <div className="flex gap-2">
                    <button
                      onClick={() => openEdit(category)}
                      className="rounded bg-slate-700 px-3 py-1 text-white hover:bg-slate-800"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(category.id)}
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
          <h2 className="text-xl font-semibold">{editing ? 'Editar categoria' : 'Crear categoria'}</h2>
          {formError ? <p className="rounded bg-red-100 p-2 text-sm text-red-700">{formError}</p> : null}
          <input
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            placeholder="Nombre"
            className={`w-full rounded border px-3 py-2 ${!isValid && nombre.length > 0 ? 'border-red-400' : 'border-slate-300'}`}
          />
          <button
            type="submit"
            disabled={!isValid || createMutation.isPending || updateMutation.isPending}
            className="w-full rounded bg-emerald-600 px-4 py-2 text-white disabled:bg-slate-400"
          >
            {createMutation.isPending || updateMutation.isPending ? 'Cargando...' : 'Guardar'}
          </button>
        </form>
      </Modal>
    </div>
  )
}

export default CategoriesPage