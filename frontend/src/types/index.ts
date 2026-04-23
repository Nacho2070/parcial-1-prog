export interface Category {
  id: number
  nombre: string
}

export interface CategoryCreateInput {
  nombre: string
}

export interface Ingredient {
  id: number
  nombre: string
}

export interface IngredientCreateInput {
  nombre: string
}

export interface Product {
  id: number
  nombre: string
  descripcion?: string | null
  precio: number
  categoria_id: number
  categoria?: Category | null
  ingredientes?: Ingredient[]
}

export interface ProductCreateInput {
  nombre: string
  descripcion?: string
  precio: number
  categoria_id: number
  ingrediente_ids: number[]
}

export interface ProductUpdateInput {
  nombre?: string
  descripcion?: string | null
  precio?: number
  categoria_id?: number
  ingrediente_ids?: number[]
}