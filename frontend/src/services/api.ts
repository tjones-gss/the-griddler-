import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface PatternMatch {
  pattern_type: string
  line_number: number
  code_snippet: string
  context?: string
}

export interface ComparisonResult {
  pre_patterns: PatternMatch[]
  post_patterns: PatternMatch[]
  transformation_rules: Array<{
    rule_id: string
    description: string
    from_pattern: string
    to_pattern: string
    confidence: number
  }>
  differences: string[]
  similarity_score: number
  analysis_method: string
  ai_insights?: string
}

export interface ConversionResult {
  converted_code: string
  applied_rules: Array<{
    rule_id: string
    description: string
    confidence: number
  }>
  warnings: string[]
  status: string
  confidence_score: number
}

export interface HealthCheck {
  status: string
  version: string
  ai_available: {
    claude: boolean
    openai: boolean
  }
}

export const apiService = {
  async healthCheck(): Promise<HealthCheck> {
    const response = await api.get<HealthCheck>('/api/health')
    return response.data
  },

  async comparePrograms(
    preCode: string,
    postCode: string,
    analysisMethod: 'code_based' | 'ai_based' = 'code_based',
    aiModel: string = 'claude'
  ): Promise<ComparisonResult> {
    const response = await api.post<ComparisonResult>('/api/compare', {
      pre_code: preCode,
      post_code: postCode,
      analysis_method: analysisMethod,
      ai_model: aiModel,
    })
    return response.data
  },

  async convertProgram(
    preCode: string,
    autoDetectRules: boolean = true,
    rules?: Array<any>
  ): Promise<ConversionResult> {
    const response = await api.post<ConversionResult>('/api/convert', {
      pre_code: preCode,
      auto_detect_rules: autoDetectRules,
      rules,
    })
    return response.data
  },
}

export default api
