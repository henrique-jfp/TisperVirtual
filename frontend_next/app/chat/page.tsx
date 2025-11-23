"use client"
import React from 'react'
import ChatWindow from '../../components/ChatWindow'

export default function ChatPage() {
  return (
    <main className="container mx-auto p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold">Chat RAG — Tipster</h1>
        <p className="text-slate-600">Converse com a IA (persona Cria do Green). Respostas baseadas no RAG.</p>
      </header>
      <section>
        <ChatWindow />
      </section>
    </main>
  )
}
