import { useState } from 'react'
import { Upload, Play, Sparkles, Code, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react'
import { apiService, ComparisonResult } from '../services/api'
import CodeEditor from '../components/CodeEditor'
import PatternList from '../components/PatternList'
import TransformationRules from '../components/TransformationRules'

interface ComparePageProps {
  isActive: boolean
}

export default function ComparePage({ isActive }: ComparePageProps) {
  const [preCode, setPreCode] = useState('')
  const [postCode, setPostCode] = useState('')
  const [analysisMethod, setAnalysisMethod] = useState<'code_based' | 'ai_based'>('code_based')
  const [aiModel, setAiModel] = useState('claude')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ComparisonResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = (type: 'pre' | 'post') => (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        const content = event.target?.result as string
        if (type === 'pre') {
          setPreCode(content)
        } else {
          setPostCode(content)
        }
      }
      reader.readAsText(file)
    }
  }

  const handleAnalyze = async () => {
    if (!preCode || !postCode) {
      setError('Please provide both PRE and POST code')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await apiService.comparePrograms(preCode, postCode, analysisMethod, aiModel)
      setResult(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  if (!isActive) return null

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Compare Programs</h2>
        <p className="text-gray-600">
          Upload PRE (REPEAT GROUPS) and POST (SCR100) programs to analyze transformation patterns
        </p>
      </div>

      {/* Upload Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* PRE Code */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">PRE Conversion</h3>
            <label className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 cursor-pointer transition-colors">
              <Upload className="w-4 h-4" />
              Upload
              <input
                type="file"
                accept=".cob,.cbl,.cobol"
                onChange={handleFileUpload('pre')}
                className="hidden"
              />
            </label>
          </div>
          <CodeEditor
            value={preCode}
            onChange={setPreCode}
            placeholder="Paste or upload PRE conversion COBOL code here..."
            height="300px"
          />
        </div>

        {/* POST Code */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">POST Conversion</h3>
            <label className="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 cursor-pointer transition-colors">
              <Upload className="w-4 h-4" />
              Upload
              <input
                type="file"
                accept=".cob,.cbl,.cobol"
                onChange={handleFileUpload('post')}
                className="hidden"
              />
            </label>
          </div>
          <CodeEditor
            value={postCode}
            onChange={setPostCode}
            placeholder="Paste or upload POST conversion COBOL code here..."
            height="300px"
          />
        </div>
      </div>

      {/* Analysis Options */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Method</h3>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="flex gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  value="code_based"
                  checked={analysisMethod === 'code_based'}
                  onChange={(e) => setAnalysisMethod(e.target.value as any)}
                  className="w-4 h-4 text-blue-600"
                />
                <Code className="w-4 h-4" />
                <span>Code-Based (Fast)</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  value="ai_based"
                  checked={analysisMethod === 'ai_based'}
                  onChange={(e) => setAnalysisMethod(e.target.value as any)}
                  className="w-4 h-4 text-blue-600"
                />
                <Sparkles className="w-4 h-4" />
                <span>AI-Based (Intelligent)</span>
              </label>
            </div>
          </div>

          {analysisMethod === 'ai_based' && (
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium text-gray-700">Model:</label>
              <select
                value={aiModel}
                onChange={(e) => setAiModel(e.target.value)}
                className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm"
              >
                <option value="claude">Claude</option>
                <option value="openai">OpenAI</option>
              </select>
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={loading || !preCode || !postCode}
            className="flex items-center justify-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                Analyze
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-red-900">Analysis Failed</h4>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle2 className="w-6 h-6 text-green-600" />
              <h3 className="text-xl font-semibold text-gray-900">Analysis Complete</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="text-sm text-blue-600 font-medium mb-1">Similarity Score</div>
                <div className="text-2xl font-bold text-blue-900">
                  {(result.similarity_score * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <div className="text-sm text-purple-600 font-medium mb-1">PRE Patterns</div>
                <div className="text-2xl font-bold text-purple-900">{result.pre_patterns.length}</div>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <div className="text-sm text-green-600 font-medium mb-1">POST Patterns</div>
                <div className="text-2xl font-bold text-green-900">{result.post_patterns.length}</div>
              </div>
            </div>
          </div>

          {/* Differences */}
          {result.differences.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Differences</h3>
              <ul className="space-y-2">
                {result.differences.map((diff, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-gray-700">
                    <span className="text-blue-600 font-bold">•</span>
                    {diff}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Transformation Rules */}
          <TransformationRules rules={result.transformation_rules} />

          {/* Patterns */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PatternList title="PRE Patterns" patterns={result.pre_patterns} color="blue" />
            <PatternList title="POST Patterns" patterns={result.post_patterns} color="green" />
          </div>

          {/* AI Insights */}
          {result.ai_insights && (
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-sm border border-purple-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-purple-600" />
                <h3 className="text-lg font-semibold text-gray-900">AI Insights</h3>
              </div>
              <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                {result.ai_insights}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
