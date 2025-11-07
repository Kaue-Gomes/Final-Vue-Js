<template>
  <div class="home-page">
    <div class="home-hero">
      <h1>Sistema de Gerenciamento de Produtos</h1>
      <p>Gerencie seus produtos de forma eficiente e profissional</p>
      <div class="home-actions">
        <router-link v-if="!isAuthenticated" to="/login" class="btn btn-primary btn-large">
          Começar Agora
        </router-link>
        <router-link v-else to="/produtos" class="btn btn-primary btn-large">
          Ir para Produtos
        </router-link>
      </div>
    </div>

    <div class="home-features">
      <div class="feature-card">
        <i class="bi bi-speedometer2"></i>
        <h3>Dashboard Completo</h3>
        <p>Visualize métricas e estatísticas em tempo real</p>
      </div>
      <div class="feature-card">
        <i class="bi bi-box-seam"></i>
        <h3>Gestão de Produtos</h3>
        <p>Gerencie todos os seus produtos com facilidade</p>
      </div>
      <div class="feature-card">
        <i class="bi bi-shield-check"></i>
        <h3>Seguro e Confiável</h3>
        <p>Sistema seguro com autenticação JWT</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style scoped>
.home-page {
  min-height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.home-hero {
  max-width: 800px;
  margin-bottom: 4rem;
}

.home-hero h1 {
  font-size: 3rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
}

.home-hero p {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin: 0 0 2rem 0;
}

.home-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.home-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  width: 100%;
}

.feature-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.feature-card i {
  font-size: 3rem;
  color: var(--color-primary);
  margin-bottom: 1rem;
  display: block;
}

.feature-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.feature-card p {
  margin: 0;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .home-hero h1 {
    font-size: 2rem;
  }

  .home-hero p {
    font-size: 1rem;
  }

  .home-features {
    grid-template-columns: 1fr;
  }
}
</style>

