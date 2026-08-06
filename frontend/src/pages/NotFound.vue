<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <section class="bg-dark text-white min-vh-100 d-flex align-items-center justify-content-center">
    <div class="text-center px-3">
      <i class="bi bi-signpost-split display-1 d-block mb-3 opacity-50"></i>
      <h1 class="display-1 fw-bold mb-2">404</h1>
      <p class="lead mb-4 opacity-75">TRAIL NOT FOUND</p>
      <button @click="router.push('/')" class="btn btn-primary btn-lg px-4">
        <i class="bi bi-arrow-left me-2"></i>Back to home
      </button>
    </div>
  </section>
</template>