import { motion } from 'framer-motion'
import { FiActivity } from 'react-icons/fi'
import { useEffect, useState } from 'react'
import { checkHealth } from '../services/api'

const Header = () => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null)

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const health = await checkHealth()
        setIsHealthy(health.lm_studio_available)
      } catch {
        setIsHealthy(false)
      }
    }
    checkStatus()
    const interval = setInterval(checkStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="glass-effect shadow-sm sticky top-0 z-50"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">P</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Prompt Optimizer</h1>
              <p className="text-xs text-gray-500">Powered by LM Studio</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <FiActivity
              className={`w-5 h-5 ${isHealthy ? 'text-green-500' : 'text-red-500'}`}
            />
            <span className="text-sm text-gray-600">
              {isHealthy === null ? 'Checking...' : isHealthy ? 'Online' : 'Offline'}
            </span>
          </div>
        </div>
      </div>
    </motion.header>
  )
}

export default Header
