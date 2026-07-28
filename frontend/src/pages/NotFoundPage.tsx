/**
 * Not Found Page — Structural Skeleton
 *
 * Rendered for all unmatched routes (path="*").
 * Scope (Sub-Phase 1.3): Structural placeholder only.
 * Full UI design implemented in Phase 7.
 */
import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <main>
      <h1>404 — Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <Link to="/">Return to Home</Link>
    </main>
  )
}

export default NotFoundPage
