import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type {
  Category,
  CategoryCreateInput,
  Ingredient,
  IngredientCreateInput,
  Product,
  ProductCreateInput,
  ProductUpdateInput,
} from '../types'
import { api } from '../utils/api'

export const useProducts = () =>
  useQuery({
    queryKey: ['productos'],
    queryFn: () => api.productos.list() as Promise<Product[]>,
  })

export const useCreateProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ProductCreateInput) => api.productos.create(payload) as Promise<Product>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export const useUpdateProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductUpdateInput }) =>
      api.productos.update(id, data) as Promise<Product>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export const useDeleteProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.productos.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export const useProductDetail = (id?: number) =>
  useQuery({
    queryKey: ['producto', id],
    queryFn: () => api.productos.detail(id as number) as Promise<Product>,
    enabled: !!id,
  })

export const useIngredients = () =>
  useQuery({
    queryKey: ['ingredientes'],
    queryFn: () => api.ingredientes.list() as Promise<Ingredient[]>,
  })

export const useCreateIngredient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: IngredientCreateInput) => api.ingredientes.create(payload) as Promise<Ingredient>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}

export const useUpdateIngredient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: IngredientCreateInput }) =>
      api.ingredientes.update(id, data) as Promise<Ingredient>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}

export const useDeleteIngredient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.ingredientes.delete(id) as Promise<{ message: string }>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}

export const useCategories = () =>
  useQuery({
    queryKey: ['categorias'],
    queryFn: () => api.categorias.list() as Promise<Category[]>,
  })

export const useCreateCategory = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CategoryCreateInput) => api.categorias.create(payload) as Promise<Category>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categorias'] }),
  })
}

export const useUpdateCategory = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: CategoryCreateInput }) =>
      api.categorias.update(id, data) as Promise<Category>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categorias'] }),
  })
}

export const useDeleteCategory = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.categorias.delete(id) as Promise<{ message: string }>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categorias'] }),
  })
}
