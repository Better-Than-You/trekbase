<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <section class="not-found-page">
    <div class="text-center">
      <h1 class="display-1 fw-bold text-light mb-2" style="letter-spacing: 6px; text-shadow: 4px 4px 8px rgba(0,0,0,0.5);">404</h1>
      <p class="text-light mb-4" style="letter-spacing: 2px; font-size: 1.1rem; text-shadow: 4px 4px 8px rgba(0,0,0,0.5);">TRAIL NOT FOUND</p>
      <button @click="router.push('/')" class="btn btn-light px-4" style="letter-spacing: 2px; color: var(--deep-space-blue);">BACK TO BASE</button>
    </div>
  </section>
</template>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--deep-space-blue);
  position: relative;
}
</style>
