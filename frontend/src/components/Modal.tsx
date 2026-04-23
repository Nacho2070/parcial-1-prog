import React from 'react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/45 p-4">
      <div className="w-full max-w-lg rounded-xl bg-white p-5 shadow-xl">
        <button
          onClick={onClose}
          className="mb-3 rounded px-2 py-1 text-sm text-slate-600 hover:bg-slate-100"
        >
          Cerrar
        </button>
        {children}
      </div>
    </div>
  )
}

export default Modal