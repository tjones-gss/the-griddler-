import { GitCompare, ArrowRightLeft, Settings } from 'lucide-react'

interface NavigationProps {
  activeTab: 'compare' | 'convert' | 'settings'
  setActiveTab: (tab: 'compare' | 'convert' | 'settings') => void
}

export default function Navigation({ activeTab, setActiveTab }: NavigationProps) {
  const tabs = [
    { id: 'compare' as const, label: 'Compare', icon: GitCompare },
    { id: 'convert' as const, label: 'Convert', icon: ArrowRightLeft },
    { id: 'settings' as const, label: 'Settings', icon: Settings },
  ]

  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex gap-1">
          {tabs.map((tab) => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center gap-2 px-6 py-3 font-medium transition-all
                  border-b-2 -mb-px
                  ${isActive
                    ? 'text-blue-600 border-blue-600 bg-blue-50'
                    : 'text-gray-600 border-transparent hover:text-gray-900 hover:bg-gray-50'
                  }
                `}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            )
          })}
        </div>
      </div>
    </nav>
  )
}
