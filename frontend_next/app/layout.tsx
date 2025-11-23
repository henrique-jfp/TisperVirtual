import '../styles/globals.css'
import React from 'react'
import { Toaster } from 'sonner'

export const metadata = {
  title: 'Tipster IA - Dicas de Apostas',
  description: 'IA especializada em dicas de apostas de futebol',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
          {children}
          <Toaster />
        </div>
      </body>
    </html>
  )
}
