<script setup>
import { useRouter } from 'vue-router'
import { state, clearAuth } from '@/store/auth'

const router = useRouter()

function handleLogout() {
  clearAuth()
  router.push('/')
}
</script>

<template>
  <nav class="navbar fixed-top border-bottom border-secondary border-opacity-25"
       style="z-index: 100; background: rgba(3, 56, 87, 0.85);">
    <div class="container">
      <router-link to="/" class="navbar-brand text-light fw-bold"
                   style="letter-spacing: 2px;">TREKBASE</router-link>

      <div class="d-flex align-items-center gap-3">
        <template v-if="state.user">
          <span class="text-light small">{{ state.user.name }}</span>
          <button @click="handleLogout" class="btn btn-outline-light btn-sm px-3"
                  style="letter-spacing: 1px;">LOGOUT</button>
        </template>
        <template v-else>
          <router-link to="/auth/login" class="btn btn-light small px-3 py-2"
                       style="color: var(--deep-space-blue); letter-spacing: 1px;">LOGIN</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav-link {
  letter-spacing: 1px;
  transition: color 0.2s;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  color: var(--parchment);
  border-bottom-color: var(--parchment);
}
</style>
