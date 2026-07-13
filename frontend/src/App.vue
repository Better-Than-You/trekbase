<script setup>
import Navbar from '@/components/Navbar.vue'
import Home from '@/pages/Home.vue'
</script>

<template>
  <!-- <Navbar /> -->
  <main>
    <Home />
  </main>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--deep-space-blue);
}
</style>
