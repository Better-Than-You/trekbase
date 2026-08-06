<script setup>
import { useRouter, useRoute } from 'vue-router'
import { state, clearAuth } from '@/store/auth'

const router = useRouter()
const route = useRoute()

function links() {
  const role = state.role
  if (role === 'admin') {
    return [
      { text: 'Dashboard', to: '/admin/dashboard', icon: 'grid-1x2' },
      { text: 'Treks', to: '/admin/treks', icon: 'compass' },
      { text: 'Trekking staff', to: '/admin/staff', icon: 'person-gear' },
      { text: 'Users', to: '/admin/users', icon: 'people' },
    ]
  }
  if (role === 'staff') {
    return [
      { text: 'Dashboard', to: '/staff/dashboard', icon: 'grid-1x2' },
    ]
  }
  return [
    { text: 'Dashboard', to: '/user/dashboard', icon: 'grid-1x2' },
    { text: 'My bookings', to: '/user/history', icon: 'journal-text' },
    { text: 'Profile', to: '/user/profile', icon: 'person-circle' },
  ]
}

function handleLogout() {
  clearAuth()
  router.push('/auth/login')
}
</script>

<template>
  <nav class="navbar navbar-dark bg-dark border-bottom border-secondary sticky-top">
    <div class="container-fluid d-flex align-items-center gap-3 flex-wrap">
      <router-link to="/" class="navbar-brand text-white fw-bold d-inline-flex align-items-center gap-2">
        <span class="bg-primary text-white d-inline-flex align-items-center justify-content-center rounded-3 p-2">
          <i class="bi bi-tree"></i>
        </span>
        TrekBase
      </router-link>

      <template v-if="state.user">
        <ul class="navbar-nav me-auto flex-row flex-wrap gap-1">
          <li class="nav-item" v-for="l in links()" :key="l.to">
            <router-link :to="l.to" class="nav-link px-3 rounded-2"
                         :class="route.path === l.to ? 'bg-primary text-white' : 'text-light'">
              <i :class="`bi bi-${l.icon} me-1`"></i>{{ l.text }}
            </router-link>
          </li>
        </ul>
        <div class="d-flex align-items-center gap-2 ms-auto">
          <button class="btn btn-sm btn-outline-light" @click="handleLogout">
            <i class="bi bi-box-arrow-right me-1"></i>Log out
          </button>
        </div>
      </template>

      <template v-else>
        <div class="ms-auto">
          <router-link to="/auth/login" class="btn btn-sm btn-outline-light">
            <i class="bi bi-box-arrow-in-right me-1"></i>Login
          </router-link>
        </div>
      </template>
    </div>
  </nav>
</template>