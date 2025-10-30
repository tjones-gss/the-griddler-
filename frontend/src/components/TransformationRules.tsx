import { ArrowRight, Sparkles } from 'lucide-react'

interface TransformationRule {
  rule_id: string
  description: string
  from_pattern: string
  to_pattern: string
  confidence: number
}

interface TransformationRulesProps {
  rules: TransformationRule[]
}

export default function TransformationRules({ rules }: TransformationRulesProps) {
  if (rules.length === 0) {
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-purple-600" />
        <h3 className="text-lg font-semibold text-gray-900">Transformation Rules</h3>
      </div>

      <div className="space-y-4">
        {rules.map((rule, idx) => (
          <div key={idx} className="border border-gray-200 rounded-lg p-4 hover:border-purple-300 transition-colors">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h4 className="font-semibold text-gray-900">{rule.rule_id}</h4>
                <p className="text-sm text-gray-600 mt-1">{rule.description}</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="text-right">
                  <div className="text-xs text-gray-500">Confidence</div>
                  <div className="text-sm font-bold text-purple-600">
                    {(rule.confidence * 100).toFixed(0)}%
                  </div>
                </div>
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center"
                  style={{
                    background: `conic-gradient(#9333ea ${rule.confidence * 360}deg, #e9d5ff ${rule.confidence * 360}deg)`
                  }}
                >
                  <div className="w-10 h-10 bg-white rounded-full" />
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3 text-sm">
              <div className="flex-1 bg-red-50 border border-red-200 rounded px-3 py-2">
                <div className="text-xs text-red-600 font-medium mb-1">FROM</div>
                <code className="text-red-900 font-mono text-xs">{rule.from_pattern}</code>
              </div>
              <ArrowRight className="w-5 h-5 text-gray-400 flex-shrink-0" />
              <div className="flex-1 bg-green-50 border border-green-200 rounded px-3 py-2">
                <div className="text-xs text-green-600 font-medium mb-1">TO</div>
                <code className="text-green-900 font-mono text-xs">{rule.to_pattern}</code>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
