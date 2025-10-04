import { useState } from 'react'
import { motion } from 'framer-motion'
import { FiZap, FiSettings } from 'react-icons/fi'
import { optimizePrompt } from '../services/api'
import { VendorType, OptimizationResult } from '../types'

interface Props {
  onOptimize: (result: OptimizationResult) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

const vendors: { id: VendorType; name: string; color: string }[] = [
  { id: 'openai', name: 'OpenAI', color: 'bg-green-500' },
  { id: 'claude', name: 'Claude', color: 'bg-orange-500' },
  { id: 'grok', name: 'Grok', color: 'bg-purple-500' },
  { id: 'gemini', name: 'Gemini', color: 'bg-blue-500' },
  { id: 'qwen', name: 'Qwen', color: 'bg-red-500' },
  { id: 'deepseek', name: 'DeepSeek', color: 'bg-indigo-500' },
]

const OptimizerForm = ({ onOptimize, isLoading, setIsLoading }: Props) => {
  const [prompt, setPrompt] = useState('')
  const [selectedVendor, setSelectedVendor] = useState<VendorType>('openai')
  const [context, setContext] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setError('')
    setIsLoading(true)

    try {
      const result = await optimizePrompt({
        prompt: prompt.trim(),
        vendor: selectedVendor,
        context: context.trim() || undefined,
      })
      onOptimize(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Optimization failed. Please check if LM Studio is running.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-effect rounded-2xl shadow-xl p-6 md:p-8"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Prompt
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter the prompt you want to optimize..."
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
            rows={6}
            disabled={isLoading}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Target Vendor
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {vendors.map((vendor) => (
              <motion.button
                key={vendor.id}
                type="button"
                onClick={() => setSelectedVendor(vendor.id)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`
                  relative px-4 py-3 rounded-lg font-medium transition-all
                  ${selectedVendor === vendor.id
                    ? 'bg-primary-500 text-white shadow-lg'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
                  }
                `}
                disabled={isLoading}
              >
                {selectedVendor === vendor.id && (
                  <motion.div
                    layoutId="vendor-indicator"
                    className={`absolute inset-0 ${vendor.color} rounded-lg opacity-20`}
                  />
                )}
                <span className="relative">{vendor.name}</span>
              </motion.button>
            ))}
          </div>
        </div>

        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <FiSettings className={`transition-transform ${showAdvanced ? 'rotate-90' : ''}`} />
            <span>Advanced Options</span>
          </button>

          {showAdvanced && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="mt-4"
            >
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Additional Context (optional)
              </label>
              <textarea
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="Provide additional context for optimization..."
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                rows={3}
                disabled={isLoading}
              />
            </motion.div>
          )}
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
          >
            {error}
          </motion.div>
        )}

        <motion.button
          type="submit"
          disabled={isLoading}
          whileHover={{ scale: isLoading ? 1 : 1.02 }}
          whileTap={{ scale: isLoading ? 1 : 0.98 }}
          className={`
            w-full py-4 rounded-lg font-semibold text-white transition-all
            flex items-center justify-center space-x-2
            ${isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-primary-500 to-blue-600 hover:from-primary-600 hover:to-blue-700 shadow-lg hover:shadow-xl'
            }
          `}
        >
          <FiZap className={isLoading ? 'animate-pulse' : ''} />
          <span>{isLoading ? 'Optimizing...' : 'Optimize Prompt'}</span>
        </motion.button>
      </form>
    </motion.div>
  )
}

export default OptimizerForm
