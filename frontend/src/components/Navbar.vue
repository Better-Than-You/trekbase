<script setup>
</script>

<template>
  <nav class="navbar fixed-top border-bottom border-secondary border-opacity-25" style="z-index: 100; background: rgba(3, 56, 87, 0.85);">
    <div class="container">
      <a href="/" class="navbar-brand text-light fw-bold" style="letter-spacing: 2px;">TREKBASE</a>

      <div class="d-flex align-items-center gap-3">
        <a href="/login" class="btn btn-light small px-3 py-2" style="color: var(--deep-space-blue)">LOGIN</a>
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
