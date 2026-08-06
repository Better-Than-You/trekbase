<script setup>
import { useRouter } from 'vue-router'
import { state } from '@/store/auth'

const router = useRouter()

function go() {
  router.push(state.token ? '/' : '/auth/login')
}
</script>

<template>
  <section class="bg-dark text-white min-vh-100 d-flex align-items-center justify-content-center">
    <div class="text-center px-3">
      <span class="text-white d-inline-flex align-items-center justify-content-center rounded-3 mb-3">
        <!-- <i class="bi bi-mountain fs-3"></i> -->
        <img src="/trekbase_logo.png" alt="TrekBase" class="d-block" style="width: 128px; height: 128px;" />

      </span>
      <h1 class="display-3 fw-bold mb-2">TrekBase</h1>
      <p class="lead mb-4 opacity-75">Plan it. Staff it. Trek it. One place to manage trek routes, assign staff and take bookings.</p>
      <div class="d-flex justify-content-center gap-2 flex-wrap">
        <router-link to="/auth/login" class="btn btn-primary btn-lg px-4">
          <i class="bi bi-box-arrow-in-right me-2"></i>Login
        </router-link>
        <router-link to="/auth/register" class="btn btn-outline-light btn-lg px-4">
          <i class="bi bi-person-plus me-2"></i>Register as Trekker
        </router-link>
      </div>
      <button class="d-none" @click="go"></button>
    </div>
  </section>
</template>