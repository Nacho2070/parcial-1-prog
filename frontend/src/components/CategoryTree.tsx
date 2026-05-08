import React, { useState } from 'react'
import type { Category } from '../types'

interface CategoryTreeProps {
  categories: Category[]
  onSelect: (categoryId: number) => void
}

interface CategoryNodeProps {
  category: Category
  level: number
  onSelect: (categoryId: number) => void
}

const CategoryNode: React.FC<CategoryNodeProps> = ({ category, level, onSelect }) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const childCategories = category.subcategorias ?? []
  const hasChildren = childCategories.length > 0

  return (
    <li>
      <div
        className="flex items-center gap-2 rounded px-2 py-1 hover:bg-slate-50"
        style={{ paddingLeft: `${level * 1.25}rem` }}
      >
        {hasChildren ? (
          <button
            type="button"
            onClick={() => setIsExpanded((prev) => !prev)}
            className="inline-flex h-6 w-6 items-center justify-center rounded border border-slate-300 text-slate-700 hover:bg-slate-100"
            aria-label={isExpanded ? `Colapsar ${category.nombre}` : `Expandir ${category.nombre}`}
          >
            {isExpanded ? '−' : '+'}
          </button>
        ) : (
          <span className="inline-flex h-6 w-6 items-center justify-center text-slate-400">•</span>
        )}

        <span className="flex-1 text-slate-800">{category.nombre}</span>

        <button
          type="button"
          onClick={() => onSelect(category.id)}
          className="rounded bg-emerald-600 px-3 py-1 text-sm text-white hover:bg-emerald-700"
        >
          Seleccionar
        </button>
      </div>

      {hasChildren && isExpanded ? (
        <ul className="mt-1">
          {childCategories.map((childCategory) => (
            <CategoryNode key={childCategory.id} category={childCategory} level={level + 1} onSelect={onSelect} />
          ))}
        </ul>
      ) : null}
    </li>
  )
}

const CategoryTree: React.FC<CategoryTreeProps> = ({ categories, onSelect }) => {
  if (!categories?.length) {
    return <p className="rounded border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600">Sin categorias.</p>
  }

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-3">
      <ul className="space-y-1">
        {categories.map((category) => (
          <CategoryNode key={category.id} category={category} level={0} onSelect={onSelect} />
        ))}
      </ul>
    </div>
  )
}

export default CategoryTree
