import { useState } from 'react'

// TODO: fetch recommended gigs from GET /match/gigs?artist_id=...
// TODO: fetch all open gigs from GET /gigs
// TODO: POST /applications when artist applies

const MOCK_GIGS = [
  {
    id: 1,
    title: 'Live Jazz for Friday Night',
    business: 'The Franklin Bar',
    category: 'Live Music',
    pay: '$200',
    date: 'Mar 21, 2026',
    match_score: 0.96,
  },
  {
    id: 2,
    title: 'Acoustic Set — Coffee Shop Opening',
    business: 'Brewed Awakening',
    category: 'Live Music',
    pay: '$150',
    date: 'Mar 28, 2026',
    match_score: 0.91,
  },
  {
    id: 3,
    title: 'Mural Commission — 8ft x 12ft',
    business: 'Old City Tattoo Co.',
    category: 'Mural/Visual Art',
    pay: '$800',
    date: 'Flexible',
    match_score: 0.72,
  },
]

export default function ArtistFeed() {
  const [applied, setApplied] = useState(new Set())

  const handleApply = (gigId) => {
    // TODO: POST /applications with { gig_id, artist_id }
    setApplied((prev) => new Set(prev).add(gigId))
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Your Gig Feed</h1>
        <p className="text-gray-500 text-sm mt-1">
          Gigs matched to your profile — ranked by semantic fit.
        </p>
      </div>

      <div className="grid gap-4">
        {MOCK_GIGS.map((gig) => (
          <div key={gig.id} className="bg-white border border-gray-100 rounded-xl p-5 shadow-sm">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h2 className="font-semibold text-gray-900">{gig.title}</h2>
                <p className="text-xs text-gray-500 mt-0.5">{gig.business} · {gig.category}</p>
              </div>
              <span className="text-sm font-bold text-brand-600 whitespace-nowrap">
                {Math.round(gig.match_score * 100)}% match
              </span>
            </div>

            <div className="flex items-center gap-4 text-xs text-gray-500 mt-3 mb-4">
              <span>💰 {gig.pay}</span>
              <span>📅 {gig.date}</span>
            </div>

            <button
              onClick={() => handleApply(gig.id)}
              disabled={applied.has(gig.id)}
              className={`w-full py-2 rounded-lg text-sm font-semibold transition-colors ${
                applied.has(gig.id)
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-brand-600 hover:bg-brand-700 text-white'
              }`}
            >
              {applied.has(gig.id) ? 'Applied!' : 'Apply'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
