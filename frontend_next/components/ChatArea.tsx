"use client"
import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Paperclip, Bot, Globe, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { toast } from 'sonner'

type Message = {
  id: string
  role: 'user' | 'assistant'
  text: string
}

export default function ChatArea() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [showSmartPrint, setShowSmartPrint] = useState(false)
  const [printUrl, setPrintUrl] = useState('')
  const [printing, setPrinting] = useState(false)
  const scrollRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const el = scrollRef.current
    if (el) {
      try {
        el.scrollTop = el.scrollHeight
      } catch (e) {
        // ignore
      }
    }
  }, [messages])

  const postMessage = async (prompt: string) => {
    // Envio otimista: mostra a mensagem do usuário imediatamente
    const userMsg: Message = { id: String(Date.now()), role: 'user', text: prompt }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    const body = { question: prompt }
    try {
      const res = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      const data = await res.json()
      const assistantMsg: Message = { id: String(Date.now() + 1), role: 'assistant', text: data.answer }
      setMessages(prev => [...prev, assistantMsg])
    } catch (err) {
      console.error(err)
      toast.error('Erro ao conectar com a IA. Verifique se o backend está rodando.')
      const errorMsg: Message = { id: String(Date.now() + 2), role: 'assistant', text: 'Erro: não foi possível obter resposta da IA.' }
      setMessages(prev => [...prev, errorMsg])
    } finally {
      setLoading(false)
    }
  }

  const handleSmartPrint = async () => {
    if (!printUrl.trim()) {
      toast.error('Digite uma URL válida')
      return
    }

    setPrinting(true)
    try {
      const res = await fetch('/api/smart-print', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: printUrl.trim() })
      })

      const data = await res.json()

      if (res.ok) {
        toast.success('Conteúdo processado com sucesso!')
        // Adicionar resultado ao chat
        const resultMsg = `📄 **Conteúdo Extraído:** ${data.data.title}\n\nTipo: ${data.data.content_type}\nConfiança: ${data.data.confidence}\n\n${data.data.data?.news_details || 'Dados estruturados salvos no banco.'}`
        setMessages(prev => [...prev, {
          id: String(Date.now()),
          role: 'assistant',
          text: resultMsg
        }])
        setPrintUrl('')
        setShowSmartPrint(false)
      } else {
        toast.error(`Erro: ${data.error}`)
      }
    } catch (err) {
      console.error(err)
      toast.error('Erro ao processar URL')
    } finally {
      setPrinting(false)
    }
  }

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault()
    if (!input.trim()) return
    postMessage(input.trim())
  }

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-gray-50 dark:bg-gray-900">
      <ScrollArea viewportRef={scrollRef} className="flex-1 p-6 h-full">
        <AnimatePresence>
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center text-gray-500 dark:text-gray-400 mt-20"
            >
              <Bot className="mx-auto h-12 w-12 mb-4" />
              <p className="text-lg">Como posso ajudar com dados do Brasileirão? (dev test)</p>
              <p className="text-sm">Pergunte sobre jogos, classificação, artilheiros ou times específicos.</p>
            </motion.div>
          )}
          {messages.map(m => (
            <motion.div
              key={m.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className={`mb-4 flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[70%] p-4 rounded-lg shadow-sm ${
                m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white'
              }`}>
                {m.role === 'assistant' && (
                  <div className="flex items-center mb-2">
                    <Avatar className="h-6 w-6 mr-2">
                      <AvatarFallback className="bg-purple-600 text-white text-xs">T</AvatarFallback>
                    </Avatar>
                    <span className="text-sm font-medium">Tipster</span>
                  </div>
                )}
                <div className="whitespace-pre-wrap">{m.text}</div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start mb-4"
          >
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
              <div className="flex items-center">
                <Avatar className="h-6 w-6 mr-2">
                  <AvatarFallback className="bg-purple-600 text-white text-xs">T</AvatarFallback>
                </Avatar>
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </ScrollArea>

      <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
        {showSmartPrint && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <Globe className="h-5 w-5 text-blue-600 mr-2" />
                <span className="font-medium text-blue-900 dark:text-blue-100">Impressão Inteligente</span>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setShowSmartPrint(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex gap-2">
              <Input
                value={printUrl}
                onChange={(e) => setPrintUrl(e.target.value)}
                placeholder="Cole a URL da notícia/estatísticas..."
                className="flex-1"
                disabled={printing}
              />
              <Button onClick={handleSmartPrint} disabled={printing || !printUrl.trim()} className="bg-blue-600 hover:bg-blue-700">
                {printing ? 'Processando...' : 'Extrair'}
              </Button>
            </div>
            <p className="text-xs text-blue-700 dark:text-blue-300 mt-2">
              Extraia dados de notícias, estatísticas e relatórios automaticamente para o banco de dados.
            </p>
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <div className="flex-1">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Pergunte sobre jogos, classificação, artilheiros..."
              className="h-[60px] resize-none"
              disabled={loading}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSubmit()
                }
              }}
            />
            <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
              <span>Pressione Enter para enviar, Shift+Enter para nova linha</span>
              <span>{input.length}/1000</span>
            </div>
          </div>
          <Button type="button" variant="outline" size="icon" className="h-12 w-12" onClick={() => setShowSmartPrint(!showSmartPrint)}>
            <Globe className="h-4 w-4" />
          </Button>
          <Button type="submit" disabled={loading || !input.trim()} className="h-12 px-6 bg-purple-600 hover:bg-purple-700">
            <Send className="h-4 w-4 mr-2" />
            Enviar
          </Button>
        </form>
      </div>
    </div>
  )
}