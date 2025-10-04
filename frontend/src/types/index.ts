export type VendorType = 'openai' | 'claude' | 'grok' | 'gemini' | 'qwen' | 'deepseek'

export interface OptimizationRequest {
  prompt: string
  vendor: VendorType
  context?: string
  max_length?: number
}

export interface OptimizationResult {
  original: string
  optimized: string
  vendor: VendorType
  enhancement_notes: string
  metadata: {
    vendor: string
    format: string
    temperature_recommendation?: string
    model_recommendation?: string
    strengths?: string[]
    features?: string[]
  }
}

export interface HealthStatus {
  status: string
  lm_studio_available: boolean
  vendor_adapters: number
}
