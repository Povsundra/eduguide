/// <reference types="vite/client" />

/**
 * Augment ImportMeta to include Vite's env variables.
 * This provides type-safe access to import.meta.env throughout the app.
 */
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  // Add future environment variables here
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
