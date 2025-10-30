import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Navigation from './components/Navigation'
import ComparePage from './pages/ComparePage'
import ConvertPage from './pages/ConvertPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  const [activeTab, setActiveTab] = useState<'compare' | 'convert' | 'settings'>('compare')

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 container mx-auto px-4 py-6 max-w-7xl">
        <Routes>
          <Route path="/" element={<ComparePage isActive={activeTab === 'compare'} />} />
          <Route path="/compare" element={<ComparePage isActive={activeTab === 'compare'} />} />
          <Route path="/convert" element={<ConvertPage isActive={activeTab === 'convert'} />} />
          <Route path="/settings" element={<SettingsPage isActive={activeTab === 'settings'} />} />
        </Routes>

        {activeTab === 'compare' && <ComparePage isActive={true} />}
        {activeTab === 'convert' && <ConvertPage isActive={true} />}
        {activeTab === 'settings' && <SettingsPage isActive={true} />}
      </main>

      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          The Griddler v0.1.0 - COBOL SCR100 Parser
        </div>
      </footer>
    </div>
  )
}

export default App
