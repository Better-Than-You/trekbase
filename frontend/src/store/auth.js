import { reactive } from 'vue'

const state = reactive({
  user: JSON.parse(localStorage.getItem('trekbase_user') || 'null'),
  token: localStorage.getItem('trekbase_token') || null,
})

function setAuth(user, token) {
  state.user = user
  state.token = token
  localStorage.setItem('trekbase_user', JSON.stringify(user))
  localStorage.setItem('trekbase_token', token)
}

function clearAuth() {
  state.user = null
  state.token = null
  localStorage.removeItem('trekbase_user')
  localStorage.removeItem('trekbase_token')
}

export { state, setAuth, clearAuth }
