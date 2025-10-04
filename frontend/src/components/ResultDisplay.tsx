import { motion } from 'framer-motion'
import { FiCopy, FiCheck, FiInfo } from 'react-icons/fi'
import { useState } from 'react'
import { OptimizationResult } from '../types'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface Props {
  result: OptimizationResult
}

const ResultDisplay = ({ result }: Props) => {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(result.optimized)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="glass-effect rounded-2xl shadow-xl p-6 md:p-8 space-y-6"
    >
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Optimized Result</h2>
        <div className="px-4 py-2 bg-primary-100 text-primary-700 rounded-lg font-medium">
          {result.vendor.toUpperCase()}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Original Prompt</h3>
          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-gray-600 whitespace-pre-wrap">{result.original}</p>
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-700">Optimized Prompt</h3>
            <motion.button
              onClick={handleCopy}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              {copied ? (
                <FiCheck className="w-5 h-5 text-green-500" />
              ) : (
                <FiCopy className="w-5 h-5 text-gray-600" />
              )}
            </motion.button>
          </div>
          <div className="relative">
            <SyntaxHighlighter
              language="markdown"
              style={vscDarkPlus}
              customStyle={{
                borderRadius: '0.5rem',
                padding: '1rem',
                fontSize: '0.875rem',
              }}
            >
              {result.optimized}
            </SyntaxHighlighter>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-start space-x-3">
            <FiInfo className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <h4 className="font-medium text-blue-900 mb-1">Enhancement Notes</h4>
              <p className="text-sm text-blue-700">{result.enhancement_notes}</p>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {result.metadata.temperature_recommendation && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium text-gray-700 mb-1">Temperature</h4>
              <p className="text-sm text-gray-600">{result.metadata.temperature_recommendation}</p>
            </div>
          )}

          {result.metadata.model_recommendation && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium text-gray-700 mb-1">Recommended Model</h4>
              <p className="text-sm text-gray-600">{result.metadata.model_recommendation}</p>
            </div>
          )}

          {result.metadata.format && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium text-gray-700 mb-1">Format</h4>
              <p className="text-sm text-gray-600 capitalize">{result.metadata.format}</p>
            </div>
          )}

          {(result.metadata.strengths || result.metadata.features) && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium text-gray-700 mb-1">
                {result.metadata.strengths ? 'Strengths' : 'Features'}
              </h4>
              <div className="flex flex-wrap gap-2 mt-2">
                {(result.metadata.strengths || result.metadata.features)?.map((item, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  )
}

export default ResultDisplay
