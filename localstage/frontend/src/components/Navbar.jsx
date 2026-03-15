import { Link } from 'react-router-dom'

// TODO: wire up real auth state (Supabase session) and logout
export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-brand-600 tracking-tight">
          LocalStage 🎸
        </Link>

        <div className="flex items-center gap-6 text-sm font-medium text-gray-600">
          {/* TODO: conditionally render based on user role */}
          <Link to="/business" className="hover:text-brand-600 transition-colors">
            Business
          </Link>
          <Link to="/artist" className="hover:text-brand-600 transition-colors">
            Artist
          </Link>
          <Link to="/login" className="hover:text-brand-600 transition-colors">
            Login
          </Link>
        </div>
      </div>
    </nav>
  )
}
