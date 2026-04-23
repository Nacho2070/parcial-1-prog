import type {
  CategoryCreateInput,
  IngredientCreateInput,
  ProductCreateInput,
  ProductUpdateInput,
} from '../types'

const API_BASE = 'http://localhost:8000'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options)
  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(errorText || 'Error en la solicitud')
  }
  return response.json() as Promise<T>
}

export const api = {
  categorias: {
    list: () => request(`${API_BASE}/categorias`),
    create: (data: CategoryCreateInput) =>
      request(`${API_BASE}/categorias`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }),
    update: (id: number, data: CategoryCreateInput) =>
      request(`${API_BASE}/categorias/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }),
    delete: (id: number) =>
      request(`${API_BASE}/categorias/${id}`, {
        method: 'DELETE',
      }),
  },
  ingredientes: {
    list: () => request(`${API_BASE}/ingredientes`),
    create: (data: IngredientCreateInput) =>
      request(`${API_BASE}/ingredientes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }),
    update: (id: number, data: IngredientCreateInput) =>
      request(`${API_BASE}/ingredientes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }),
    delete: (id: number) =>
      request(`${API_BASE}/ingredientes/${id}`, {
        method: 'DELETE',
      }),
  },
  productos: {
    list: () => request(`${API_BASE}/productos`),
    detail: (id: number) => request(`${API_BASE}/productos/${id}`),
    create: (data: ProductCreateInput) =>
      request(`${API_BASE}/productos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }),
    update: (id: number, data: ProductUpdateInput) =>
      request(`${API_BASE}/productos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }),
    delete: (id: number) =>
      request(`${API_BASE}/productos/${id}`, {
        method: 'DELETE',
      }),
  },
}