import { useState } from 'react'
import { Upload, Play, Download, AlertCircle, CheckCircle2, Loader2, AlertTriangle } from 'lucide-react'
import { apiService, ConversionResult } from '../services/api'
import CodeEditor from '../components/CodeEditor'

interface ConvertPageProps {
  isActive: boolean
}

export default function ConvertPage({ isActive }: ConvertPageProps) {
  const [preCode, setPreCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ConversionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        const content = event.target?.result as string
        setPreCode(content)
        setResult(null)
        setError(null)
      }
      reader.readAsText(file)
    }
  }

  const handleConvert = async () => {
    if (!preCode) {
      setError('Please provide PRE conversion code')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await apiService.convertProgram(preCode, true)
      setResult(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Conversion failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (!result?.converted_code) return

    const blob = new Blob([result.converted_code], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'converted_scr100.cbl'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (!isActive) return null

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Convert to SCR100</h2>
        <p className="text-gray-600">
          Upload a PRE conversion program to automatically convert it to use SCR100 grid logic
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">PRE Conversion Code</h3>
          <label className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 cursor-pointer transition-colors">
            <Upload className="w-4 h-4" />
            Upload COBOL File
            <input
              type="file"
              accept=".cob,.cbl,.cobol"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>
        <CodeEditor
          value={preCode}
          onChange={setPreCode}
          placeholder="Paste or upload PRE conversion COBOL code here..."
          height="400px"
        />

        <div className="mt-4 flex justify-end">
          <button
            onClick={handleConvert}
            disabled={loading || !preCode}
            className="flex items-center justify-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Converting...
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                Convert to SCR100
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
            <h4 className="font-semibold text-red-900">Conversion Failed</h4>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Status */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                {result.status === 'completed' ? (
                  <>
                    <CheckCircle2 className="w-6 h-6 text-green-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Conversion Complete</h3>
                  </>
                ) : (
                  <>
                    <AlertCircle className="w-6 h-6 text-red-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Conversion Failed</h3>
                  </>
                )}
              </div>
              {result.status === 'completed' && (
                <button
                  onClick={handleDownload}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="text-sm text-blue-600 font-medium mb-1">Confidence Score</div>
                <div className="text-2xl font-bold text-blue-900">
                  {(result.confidence_score * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <div className="text-sm text-purple-600 font-medium mb-1">Rules Applied</div>
                <div className="text-2xl font-bold text-purple-900">{result.applied_rules.length}</div>
              </div>
              <div className="bg-orange-50 rounded-lg p-4">
                <div className="text-sm text-orange-600 font-medium mb-1">Warnings</div>
                <div className="text-2xl font-bold text-orange-900">{result.warnings.length}</div>
              </div>
            </div>
          </div>

          {/* Applied Rules */}
          {result.applied_rules.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Applied Transformation Rules</h3>
              <div className="space-y-3">
                {result.applied_rules.map((rule, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                    <CheckCircle2 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{rule.rule_id}</div>
                      <div className="text-sm text-gray-600">{rule.description}</div>
                    </div>
                    <div className="text-sm font-medium text-blue-600">
                      {(rule.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warnings */}
          {result.warnings.length > 0 && (
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <AlertTriangle className="w-5 h-5 text-orange-600" />
                <h4 className="font-semibold text-orange-900">Warnings</h4>
              </div>
              <ul className="space-y-2">
                {result.warnings.map((warning, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-orange-700 text-sm">
                    <span className="text-orange-600 font-bold">•</span>
                    {warning}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Converted Code */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Converted Code</h3>
            <CodeEditor
              value={result.converted_code}
              onChange={() => {}}
              readOnly
              height="500px"
            />
          </div>
        </div>
      )}
    </div>
  )
}
