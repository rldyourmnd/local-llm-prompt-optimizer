import { motion } from 'framer-motion'
import { FiGithub, FiMail, FiSend } from 'react-icons/fi'

const Footer = () => {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5 }}
      className="mt-16 border-t border-gray-200 bg-white/50"
    >
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8 text-center md:text-left">
          <div>
            <h3 className="font-bold text-gray-900 mb-2">About</h3>
            <p className="text-sm text-gray-600">
              Local-first prompt optimization for multiple LLM vendors
            </p>
          </div>

          <div>
            <h3 className="font-bold text-gray-900 mb-2">Credits</h3>
            <p className="text-sm text-gray-600">
              Created by <strong>Danil Silantyev</strong>
              <br />
              <a
                href="https://nddev.tech"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:underline"
              >
                NDDev OpenNetwork
              </a>
            </p>
          </div>

          <div>
            <h3 className="font-bold text-gray-900 mb-2">Contact</h3>
            <div className="flex justify-center md:justify-start space-x-4">
              <a
                href="https://github.com/rldyourmnd/local-llm-prompt-optimizer"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-primary-600 transition-colors"
              >
                <FiGithub className="w-5 h-5" />
              </a>
              <a
                href="https://t.me/Danil_Silantyev"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-primary-600 transition-colors"
              >
                <FiSend className="w-5 h-5" />
              </a>
              <a
                href="mailto:business@nddev.tech"
                className="text-gray-600 hover:text-primary-600 transition-colors"
              >
                <FiMail className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>© 2025 NDDev OpenNetwork. All rights reserved.</p>
        </div>
      </div>
    </motion.footer>
  )
}

export default Footer
