<template>
  <footer class="footer">
    <div class="footer-content">
      <p>&copy; {{ ano }} Sistema de Gerenciamento de Produtos. Todos os direitos reservados.</p>
      <div class="footer-links">
        <router-link to="/sobre">Sobre</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const ano = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background: var(--bg-primary);
  border-top: 1px solid var(--border-color);
  padding: 2rem 1.5rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-content p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: var(--color-primary);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>

