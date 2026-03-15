import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'

// TODO: fetch real gigs from GET /gigs?business_id=...
// TODO: fetch recommended artists from GET /match/artists?gig_id=...
const MOCK_GIGS = [
  { id: 1, title: 'Live Jazz for Friday Night', category: 'Live Music', status: 'open', applicants: 3 },
  { id: 2, title: 'Mural for Coffee Shop Wall', category: 'Mural/Visual Art', status: 'open', applicants: 7 },
]

const MOCK_ARTISTS = [
  { id: 1, name: 'Maya Chen', category: 'Jazz Musician', match_score: 0.94 },
  { id: 2, name: 'DeShawn Morris', category: 'Muralist', match_score: 0.91 },
  { id: 3, name: 'Sofia Reyes', category: 'Photographer', match_score: 0.87 },
]

export default function BusinessDashboard() {
  const [gigs] = useState(MOCK_GIGS)
  const [recommended] = useState(MOCK_ARTISTS)

  // TODO: useEffect to load real data from API

  return (
    <div className="space-y-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Business Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">Manage your gigs and discover local talent.</p>
        </div>
        <Link
          to="/business/post-gig"
          className="bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors"
        >
          + Post a Gig
        </Link>
      </div>

      {/* Active Gigs */}
      <section>
        <h2 className="text-lg font-semibold text-gray-800 mb-3">Your Active Gigs</h2>
        {gigs.length === 0 ? (
          <p className="text-gray-400 text-sm">No gigs posted yet.</p>
        ) : (
          <div className="grid gap-4">
            {gigs.map((gig) => (
              <div key={gig.id} className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{gig.title}</p>
                  <p className="text-xs text-gray-500 mt-0.5">{gig.category} · {gig.applicants} applicants</p>
                </div>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium capitalize">
                  {gig.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* AI-Recommended Artists */}
      <section>
        <h2 className="text-lg font-semibold text-gray-800 mb-1">Recommended Artists</h2>
        <p className="text-xs text-gray-400 mb-3">Matched via semantic similarity — not just keywords.</p>
        <div className="grid gap-3">
          {recommended.map((artist) => (
            <div key={artist.id} className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">{artist.name}</p>
                <p className="text-xs text-gray-500">{artist.category}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-brand-600">{Math.round(artist.match_score * 100)}% match</p>
                {/* TODO: link to artist profile */}
                <button className="text-xs text-gray-400 hover:text-brand-500 mt-0.5">View profile →</button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
