"use client"
import * as Dialog from '@radix-ui/react-dialog'
import React from 'react'

export default function AccessibleDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger className="px-3 py-2 bg-accent text-white rounded">Abrir diálogo</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed left-1/2 top-1/2 w-11/12 max-w-md -translate-x-1/2 -translate-y-1/2 bg-white rounded p-6">
          <Dialog.Title className="text-lg font-semibold">Dialogo acessível</Dialog.Title>
          <Dialog.Description className="text-slate-600">Exemplo usando Radix primitives</Dialog.Description>
          <div className="mt-4">
            <button className="px-3 py-2 bg-primary text-white rounded">Fechar</button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
