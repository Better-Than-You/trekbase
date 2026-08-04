<script setup>
import { useRouter } from 'vue-router'
import { state, clearAuth } from '@/store/auth'

const router = useRouter()

const navbarClass = {
  admin: 'bg-black',
  user: 'bg-primary',
  staff: 'bg-success',
}[state.role] || 'bg-primary'

function handleLogout() {
  clearAuth()
  router.push('/')
}
</script>

<template>
  <nav class="navbar fixed-top border-bottom border-white border-opacity-25" :class="navbarClass">
    <div class="container">
      <router-link to="/" class="navbar-brand text-light fw-bold text-decoration-none"
                   style="letter-spacing: 2px;">TREKBASE</router-link>

      <div class="d-flex align-items-center gap-3">
        <template v-if="state.user">
          <router-link to="/admin/dashboard" class="text-light text-decoration-none small"
                       style="letter-spacing: 1px;">DASHBOARD</router-link>
          <span class="text-light small">{{ state.user.name }}</span>
          <button @click="handleLogout" class="btn btn-outline-light btn-sm px-3"
                  style="letter-spacing: 1px;">LOGOUT</button>
        </template>
        <template v-else>
          <router-link to="/auth/login" class="btn btn-light btn-sm px-3 py-2 text-decoration-none text-dark"
                       style="letter-spacing: 1px;">LOGIN</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>
