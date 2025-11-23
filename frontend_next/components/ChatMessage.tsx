import React from 'react'
import { motion } from 'framer-motion'

export default function ChatMessage({ role, text }: { role: 'user' | 'assistant', text: string }) {
  const isUser = role === 'user'
  return (
    <motion.div
      className={`mb-3 flex ${isUser ? 'justify-end' : 'justify-start'}`}
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.2 }}
    >
      <div
        className={`max-w-[80%] p-3 rounded-lg shadow-sm ${
          isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-900'
        }`}
        role="article"
        aria-label={`${isUser ? 'Sua mensagem' : 'Resposta da IA'}: ${text.slice(0, 50)}...`}
      >
        <div className="text-sm whitespace-pre-wrap">{text}</div>
      </div>
    </motion.div>
  )
}
