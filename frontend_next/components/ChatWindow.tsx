"use client"
import React, { useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ChatMessage from './ChatMessage'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'

type Message = {
  id: string
  role: 'user' | 'assistant'
  text: string
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef<HTMLDivElement | null>(null)

  const postMessage = async (prompt: string) => {
    setLoading(true)
    const body = { question: prompt }
    try {
      const res = await fetch('http://127.0.0.1:5000/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      const data = await res.json()
      const assistantMsg: Message = { id: String(Date.now()), role: 'assistant', text: data.answer }
      setMessages(prev => [...prev, { id: String(Date.now()+1), role: 'user', text: prompt }, assistantMsg])
      setInput('')
      // scroll
      setTimeout(() => scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' }), 50)
    } catch (err) {
      console.error(err)
      setMessages(prev => [...prev, { id: String(Date.now()), role: 'assistant', text: 'Erro ao contatar backend.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault()
    if (!input.trim()) return
    postMessage(input.trim())
  }

  return (
    <Card className="w-full max-w-2xl mx-auto h-[600px] flex flex-col">
      <CardHeader>
        <CardTitle className="text-center">Tipster de Futebol - Chat IA</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col gap-4 p-4">
        <ScrollArea viewportRef={scrollRef} className="flex-1 h-96 rounded-md border p-4" role="log" aria-live="polite" aria-label="Histórico de mensagens">
          <AnimatePresence>
            {messages.length === 0 && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="text-slate-500 text-center"
              >
                Nenhuma mensagem. Pergunte algo sobre futebol (Série A 2025).
              </motion.p>
            )}
            {messages.map(m => (
              <motion.div
                key={m.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <ChatMessage role={m.role} text={m.text} />
              </motion.div>
            ))}
          </AnimatePresence>
        </ScrollArea>

        <form onSubmit={handleSubmit} className="flex gap-2" aria-label="Formulário de envio de mensagens">
          <Input
            id="chat-input"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Digite sua pergunta..."
            aria-required="true"
            className="flex-1"
            disabled={loading}
          />
          <Button type="submit" disabled={loading || !input.trim()} aria-disabled={loading}>
            {loading ? 'Enviando...' : 'Enviar'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
