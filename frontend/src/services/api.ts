import axios from 'axios'
import { OptimizationRequest, OptimizationResult, HealthStatus } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const optimizePrompt = async (request: OptimizationRequest): Promise<OptimizationResult> => {
  const response = await api.post<OptimizationResult>('/api/optimize', request)
  return response.data
}

export const checkHealth = async (): Promise<HealthStatus> => {
  const response = await api.get<HealthStatus>('/health')
  return response.data
}

export default api
