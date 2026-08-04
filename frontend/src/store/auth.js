import { reactive } from 'vue'

const initialUser = JSON.parse(localStorage.getItem('trekbase_user') || 'null')

const state = reactive({
  user: initialUser,
  token: localStorage.getItem('trekbase_token') || null,
  role: initialUser?.role || 'user',
})

function setAuth(user, token) {
  state.user = user
  state.token = token
  state.role = user.role || 'user'
  localStorage.setItem('trekbase_user', JSON.stringify(user))
  localStorage.setItem('trekbase_token', token)
}

function clearAuth() {
  state.user = null
  state.token = null
  state.role = 'user'
  localStorage.removeItem('trekbase_user')
  localStorage.removeItem('trekbase_token')
}

export { state, setAuth, clearAuth }