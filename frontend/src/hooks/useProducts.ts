import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../utils/api'
import type { Product, ProductCreateInput, ProductUpdateInput } from '../types'

export const useProducts = () => {
  return useQuery({
    queryKey: ['productos'],
    queryFn: () => api.productos.list() as Promise<Product[]>,
  })
}

export const useCreateProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ProductCreateInput) =>
      api.productos.create(payload) as Promise<Product>,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
}

export const useUpdateProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductUpdateInput }) =>
      api.productos.update(id, data) as Promise<Product>,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
}

export const useDeleteProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.productos.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] })
    },
  })
}

export const useProductDetail = (id?: number) => {
  return useQuery({
    queryKey: ['producto', id],
    queryFn: () => api.productos.detail(id!) as Promise<Product>,
    enabled: !!id,
  })
}