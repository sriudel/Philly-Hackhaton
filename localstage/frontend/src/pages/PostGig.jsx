import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const CATEGORIES = [
  'Live Music',
  'Mural/Visual Art',
  'Photography',
  'Influencer/Social Media',
  'DJ',
  'Dance Performance',
  'Other',
]

// TODO: POST /gigs with form data
// TODO: after posting, trigger embedding generation on the backend
export default function PostGig() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    title: '',
    category: '',
    description: '',
    pay: '',
    date: '',
    location: '',
  })

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    // TODO: POST to /api/gigs and handle response
    console.log('Posting gig:', form)
    navigate('/business')
  }

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Post a Gig</h1>
      <p className="text-gray-500 text-sm mb-6">
        Describe what you need — we'll match you with the best local talent.
      </p>

      <form onSubmit={handleSubmit} className="bg-white border border-gray-100 rounded-xl p-6 shadow-sm space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Gig Title</label>
          <input
            name="title"
            required
            value={form.title}
            onChange={handleChange}
            placeholder="e.g. Live Jazz for Friday Night"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select
            name="category"
            required
            value={form.category}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            <option value="">Select a category</option>
            {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            name="description"
            required
            rows={4}
            value={form.description}
            onChange={handleChange}
            placeholder="Describe the vibe, venue size, style preferences, what you're looking for..."
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 resize-none"
          />
          <p className="text-xs text-gray-400 mt-1">
            Be descriptive — this text is used for AI matching.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Pay</label>
            <input
              name="pay"
              value={form.pay}
              onChange={handleChange}
              placeholder="e.g. $200 or negotiable"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              type="date"
              name="date"
              value={form.date}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
          <input
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="e.g. Old City, Philadelphia"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2 rounded-lg transition-colors"
        >
          Post Gig
        </button>
      </form>
    </div>
  )
}
