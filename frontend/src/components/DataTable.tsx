import React from 'react'

interface Column<T> {
  key: keyof T
  header: string
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  onEdit: (item: T) => void
  onDelete: (id: number) => void
}

function DataTable<T extends { id?: number }>({ data, columns, onEdit, onDelete }: DataTableProps<T>) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map(col => <th key={col.key as string}>{col.header}</th>)}
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={item.id}>
            {columns.map(col => <td key={col.key as string}>{item[col.key] as React.ReactNode}</td>)}
            <td>
              <button onClick={() => onEdit(item)}>Edit</button>
              <button onClick={() => item.id && onDelete(item.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default DataTable