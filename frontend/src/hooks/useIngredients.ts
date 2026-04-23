import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../utils/api'
import type { Ingredient, IngredientCreateInput } from '../types'

export const useIngredients = () => {
  return useQuery({
    queryKey: ['ingredientes'],
    queryFn: () => api.ingredientes.list() as Promise<Ingredient[]>,
  })
}

export const useCreateIngredient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: IngredientCreateInput) =>
      api.ingredientes.create(payload) as Promise<Ingredient>,
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
    mutationFn: (id: number) => api.ingredientes.delete(id) as unknown as Promise<{ message: string }>,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}