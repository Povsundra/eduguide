/**
 * EduGuide Application Entry Point
 *
 * Wraps the root App component with BrowserRouter to enable
 * client-side routing throughout the application.
 */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App'

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error(
    'Root element with id "root" not found. Check index.html.'
  )
}

createRoot(rootElement).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
)
