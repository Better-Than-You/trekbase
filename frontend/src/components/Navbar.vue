<script setup>
import { useRouter, useRoute } from 'vue-router'
import { state, clearAuth } from '@/store/auth'

const router = useRouter()
const route = useRoute()

function handleLogout() {
  clearAuth()
  router.push('/')
}
</script>

<template>
  <!-- admin navbar: black -->
  <nav v-if="state.user && state.role === 'admin'"
       class="navbar fixed-top border-bottom border-white border-opacity-25 bg-black">
    <div class="container">
      <router-link to="/" class="navbar-brand text-light fw-bold text-decoration-none"
                   style="letter-spacing: 2px;">TREKBASE</router-link>

      <div class="d-flex align-items-center gap-2">
        <router-link to="/admin/dashboard" class="btn btn-sm px-2"
                     :class="route.name === 'admin_dashboard' ? 'btn-light text-dark' : 'btn-outline-light'"
                     style="letter-spacing: 1px;">DASHBOARD</router-link>
        <button type="button" class="btn btn-outline-light btn-sm px-2"
                style="letter-spacing: 1px;">BOOKING HISTORY</button>
        <button type="button" class="btn btn-outline-light btn-sm px-2"
                style="letter-spacing: 1px;">USERLIST</button>
        <button type="button" class="btn btn-outline-light btn-sm px-2"
                style="letter-spacing: 1px;">STAFFLIST</button>
        <button @click="handleLogout" class="btn btn-outline-light btn-sm px-2"
                style="letter-spacing: 1px;">LOGOUT</button>
      </div>
    </div>
  </nav>

  <!-- user navbar: blue -->
  <nav v-else-if="state.user && state.role === 'user'"
       class="navbar fixed-top border-bottom border-white border-opacity-25 bg-primary">
    <div class="container">
      <router-link to="/" class="navbar-brand text-light fw-bold text-decoration-none"
                   style="letter-spacing: 2px;">TREKBASE</router-link>

      <div class="d-flex align-items-center gap-2">
        <span class="text-light small">{{ state.user.name }}</span>
        <button @click="handleLogout" class="btn btn-outline-light btn-sm px-2"
                style="letter-spacing: 1px;">LOGOUT</button>
      </div>
    </div>
  </nav>

  <!-- staff navbar: green -->
  <nav v-else-if="state.user && state.role === 'staff'"
       class="navbar fixed-top border-bottom border-white border-opacity-25 bg-success">
    <div class="container">
      <router-link to="/" class="navbar-brand text-light fw-bold text-decoration-none"
                   style="letter-spacing: 2px;">TREKBASE</router-link>

      <div class="d-flex align-items-center gap-2">
        <span class="text-light small">{{ state.user.name }}</span>
        <button @click="handleLogout" class="btn btn-outline-light btn-sm px-2"
                style="letter-spacing: 1px;">LOGOUT</button>
      </div>
    </div>
  </nav>

  <!-- logged out navbar: blue -->
  <nav v-else class="navbar fixed-top border-bottom border-white border-opacity-25 bg-primary">
    <div class="container">
      <router-link to="/" class="navbar-brand text-light fw-bold text-decoration-none"
                   style="letter-spacing: 2px;">TREKBASE</router-link>

      <div class="d-flex align-items-center gap-2">
        <router-link to="/auth/login" class="btn btn-light btn-sm px-3 text-decoration-none text-dark"
                     style="letter-spacing: 1px;">LOGIN</router-link>
      </div>
    </div>
  </nav>
</template>