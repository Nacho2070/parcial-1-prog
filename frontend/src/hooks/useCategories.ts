import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../utils/api'
import type { Category, CategoryCreateInput } from '../types'

export const useCategories = () => {
  return useQuery({
    queryKey: ['categorias'],
    queryFn: () => api.categorias.list() as Promise<Category[]>,
  })
}

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