import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import OptimizerForm from './components/OptimizerForm'
import ResultDisplay from './components/ResultDisplay'
import Header from './components/Header'
import Footer from './components/Footer'
import { OptimizationResult } from './types'

function App() {
  const [result, setResult] = useState<OptimizationResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleOptimize = (optimizationResult: OptimizationResult) => {
    setResult(optimizationResult)
  }

  return (
    <div className="min-h-screen gradient-bg">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-8"
        >
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
              Local LLM Prompt Optimizer
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Optimize your prompts for different LLM vendors with AI-powered enhancements
            </p>
          </div>

          <OptimizerForm
            onOptimize={handleOptimize}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />

          <AnimatePresence mode="wait">
            {result && (
              <ResultDisplay result={result} />
            )}
          </AnimatePresence>
        </motion.div>
      </main>

      <Footer />
    </div>
  )
}

export default App
