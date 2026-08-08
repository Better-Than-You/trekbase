import { reactive } from 'vue'

const initialUser = JSON.parse(localStorage.getItem('trekbase_user') || 'null')


/* documentation
const count = ref(1)
const obj = reactive({ count })

// ref will be unwrapped
console.log(obj.count === count.value) // true

// it will update `obj.count`
count.value++
console.log(count.value) // 2
console.log(obj.count) // 2

// it will also update `count` ref
obj.count++
console.log(obj.count) // 3
console.log(count.value) // 3
*/


// using reactive object for auth states
const state = reactive({
  user: initialUser,
  token: localStorage.getItem('trekbase_token') || null,
  refreshToken: localStorage.getItem('trekbase_refresh_token') || null,
  role: initialUser?.role || 'user',
})

function setAuth(user, token, refreshToken) {
  state.user = user
  state.token = token
  state.refreshToken = refreshToken || null
  state.role = user.role || 'user'
  localStorage.setItem('trekbase_user', JSON.stringify(user))
  localStorage.setItem('trekbase_token', token)
  localStorage.setItem('trekbase_refresh_token', refreshToken)
}

function clearAuth() {
  state.user = null
  state.token = null
  state.refreshToken = null
  state.role = 'user'
  localStorage.removeItem('trekbase_user')
  localStorage.removeItem('trekbase_token')
  localStorage.removeItem('trekbase_refresh_token')
}

export { state, setAuth, clearAuth }