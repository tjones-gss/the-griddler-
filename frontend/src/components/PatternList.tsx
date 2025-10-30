import { PatternMatch } from '../services/api'
import { FileCode } from 'lucide-react'

interface PatternListProps {
  title: string
  patterns: PatternMatch[]
  color: 'blue' | 'green' | 'purple'
}

export default function PatternList({ title, patterns, color }: PatternListProps) {
  const colorClasses = {
    blue: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-900',
      badge: 'bg-blue-100 text-blue-700',
      icon: 'text-blue-600'
    },
    green: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      text: 'text-green-900',
      badge: 'bg-green-100 text-green-700',
      icon: 'text-green-600'
    },
    purple: {
      bg: 'bg-purple-50',
      border: 'border-purple-200',
      text: 'text-purple-900',
      badge: 'bg-purple-100 text-purple-700',
      icon: 'text-purple-600'
    }
  }

  const classes = colorClasses[color]

  return (
    <div className={`rounded-lg shadow-sm border ${classes.border} ${classes.bg} p-6`}>
      <div className="flex items-center gap-2 mb-4">
        <FileCode className={`w-5 h-5 ${classes.icon}`} />
        <h3 className={`text-lg font-semibold ${classes.text}`}>{title}</h3>
        <span className={`ml-auto px-2 py-1 ${classes.badge} rounded-full text-sm font-medium`}>
          {patterns.length}
        </span>
      </div>

      {patterns.length === 0 ? (
        <p className="text-gray-500 text-sm">No patterns detected</p>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {patterns.map((pattern, idx) => (
            <div key={idx} className="bg-white rounded-lg p-3 border border-gray-200">
              <div className="flex items-start justify-between mb-2">
                <span className={`text-xs font-medium ${classes.badge} px-2 py-1 rounded`}>
                  {pattern.pattern_type}
                </span>
                <span className="text-xs text-gray-500">Line {pattern.line_number}</span>
              </div>
              <pre className="text-xs font-mono text-gray-800 overflow-x-auto">
                {pattern.code_snippet}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
