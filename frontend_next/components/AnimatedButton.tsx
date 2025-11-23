"use client"
import { motion } from 'framer-motion'
import React from 'react'

export default function AnimatedButton() {
  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      className="inline-flex items-center px-4 py-2 bg-primary text-white rounded-md shadow"
      aria-label="Botão animado exemplo"
    >
      Clique-me
    </motion.button>
  )
}
