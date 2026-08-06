// shared badge helpers: map an entity's status/difficulty to a bootstrap bg class
// each returns a default 'bg-secondary' fallback for unknown values

export function difficultyBadge(d) {
  return ({ easy: 'bg-success', moderate: 'bg-warning text-dark', hard: 'bg-danger' })[d] || 'bg-secondary'
}

export function statusBadge(s) {
  return ({
    pending: 'bg-secondary', approved: 'bg-info text-dark', open: 'bg-success',
    closed: 'bg-secondary', completed: 'bg-primary',
  })[s] || 'bg-secondary'
}

export function bookingBadge(s) {
  return ({ booked: 'bg-primary', cancelled: 'bg-danger', completed: 'bg-success' })[s] || 'bg-secondary'
}

export function staffBadge(s) {
  return ({
    available: 'bg-success', assigned: 'bg-primary',
    not_working: 'bg-secondary', not_available: 'bg-secondary',
  })[s] || 'bg-secondary'
}
