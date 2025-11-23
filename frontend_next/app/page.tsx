"use client"
import React, { useState } from 'react'
import Header from '../components/Header'
import Sidebar from '../components/Sidebar'
import ChatArea from '../components/ChatArea'

export default function Home() {
  const [darkMode, setDarkMode] = useState(false)

  return (
    <div className={`h-screen flex overflow-hidden ${darkMode ? 'dark' : ''}`}>
      <Sidebar />
      <div className="flex-1 flex flex-col min-h-0">
        <Header darkMode={darkMode} setDarkMode={setDarkMode} />
        <ChatArea />
      </div>
    </div>
  )
}
