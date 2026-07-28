/**
 * EduGuide Root Application Component
 *
 * Declares the client-side route tree.
 * Routes are expanded in Phase 7 (Frontend Application).
 *
 * Current routes:
 *   /           → HomePage
 *   *           → NotFoundPage (catches all unmatched paths)
 */
import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default App
