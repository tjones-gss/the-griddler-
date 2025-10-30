import { useState, useEffect } from 'react'
import { CheckCircle2, XCircle, Sparkles, Server, Info } from 'lucide-react'
import { apiService, HealthCheck } from '../services/api'

interface SettingsPageProps {
  isActive: boolean
}

export default function SettingsPage({ isActive }: SettingsPageProps) {
  const [health, setHealth] = useState<HealthCheck | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (isActive) {
      loadHealth()
    }
  }, [isActive])

  const loadHealth = async () => {
    setLoading(true)
    try {
      const data = await apiService.healthCheck()
      setHealth(data)
    } catch (err) {
      console.error('Health check failed:', err)
    } finally {
      setLoading(false)
    }
  }

  if (!isActive) return null

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Settings & Status</h2>
        <p className="text-gray-600">
          View system status and configuration options
        </p>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Server className="w-5 h-5 text-gray-700" />
          <h3 className="text-lg font-semibold text-gray-900">System Status</h3>
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : health ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-6 h-6 text-green-600" />
                <div>
                  <div className="font-medium text-gray-900">Backend API</div>
                  <div className="text-sm text-gray-600">Version {health.version}</div>
                </div>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                {health.status}
              </span>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3 p-4 bg-red-50 rounded-lg">
            <XCircle className="w-6 h-6 text-red-600" />
            <div>
              <div className="font-medium text-gray-900">Backend Unavailable</div>
              <div className="text-sm text-gray-600">Cannot connect to API server</div>
            </div>
          </div>
        )}
      </div>

      {/* AI Configuration */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-5 h-5 text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900">AI Analysis</h3>
        </div>

        {health && (
          <div className="space-y-3">
            <div className={`flex items-center justify-between p-4 rounded-lg ${
              health.ai_available.claude ? 'bg-green-50' : 'bg-gray-50'
            }`}>
              <div className="flex items-center gap-3">
                {health.ai_available.claude ? (
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-gray-400" />
                )}
                <div>
                  <div className="font-medium text-gray-900">Claude API</div>
                  <div className="text-sm text-gray-600">Anthropic's AI model</div>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                health.ai_available.claude
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {health.ai_available.claude ? 'Available' : 'Not Configured'}
              </span>
            </div>

            <div className={`flex items-center justify-between p-4 rounded-lg ${
              health.ai_available.openai ? 'bg-green-50' : 'bg-gray-50'
            }`}>
              <div className="flex items-center gap-3">
                {health.ai_available.openai ? (
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-gray-400" />
                )}
                <div>
                  <div className="font-medium text-gray-900">OpenAI API</div>
                  <div className="text-sm text-gray-600">GPT models</div>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                health.ai_available.openai
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {health.ai_available.openai ? 'Available' : 'Not Configured'}
              </span>
            </div>
          </div>
        )}

        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-blue-900">
              <p className="font-medium mb-1">Configuring AI APIs</p>
              <p className="text-blue-700">
                To enable AI-based analysis, add your API keys to the <code className="px-1 py-0.5 bg-blue-100 rounded">backend/.env</code> file:
              </p>
              <pre className="mt-2 p-2 bg-blue-100 rounded text-xs overflow-x-auto">
                ANTHROPIC_API_KEY=your_key_here{'\n'}
                OPENAI_API_KEY=your_key_here
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* About */}
      <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg shadow-sm border border-blue-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">About The Griddler</h3>
        <div className="space-y-2 text-gray-700">
          <p>
            <strong>The Griddler</strong> is an adaptable parser system for analyzing and converting
            COBOL programs from REPEAT GROUPS logic to SCR100 grid logic.
          </p>
          <p className="text-sm">
            This tool provides both code-based pattern matching and AI-assisted intelligent analysis
            to help modernize legacy COBOL applications.
          </p>
        </div>
        <div className="mt-4 pt-4 border-t border-blue-200">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Version:</span>
              <span className="ml-2 font-medium">{health?.version || '0.1.0'}</span>
            </div>
            <div>
              <span className="text-gray-600">Tech Stack:</span>
              <span className="ml-2 font-medium">Python + React</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
