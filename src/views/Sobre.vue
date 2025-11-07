<template>
  <div class="sobre-page">
    <div class="page-header">
      <h1>Sobre o Sistema</h1>
    </div>

    <div class="sobre-content">
      <div class="sobre-card">
        <h2>Sistema de Gerenciamento de Produtos</h2>
        <p>
          Sistema completo desenvolvido com Vue.js 3 e Flask para gerenciamento
          eficiente de produtos. Inclui funcionalidades de autenticação, CRUD completo,
          dashboard com métricas e interface moderna e responsiva.
        </p>

        <h3>Tecnologias Utilizadas</h3>
        <ul>
          <li><strong>Frontend:</strong> Vue.js 3, Vue Router, Pinia, Axios</li>
          <li><strong>Backend:</strong> Flask, SQLAlchemy, JWT</li>
          <li><strong>Estilização:</strong> CSS Moderno com variáveis e temas</li>
        </ul>

        <h3>Funcionalidades</h3>
        <ul>
          <li>Sistema de autenticação completo</li>
          <li>CRUD de produtos</li>
          <li>Dashboard com métricas</li>
          <li>Filtros e busca avançada</li>
          <li>Tema claro/escuro</li>
          <li>Interface responsiva</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.sobre-page {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.sobre-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
}

.sobre-card h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.sobre-card h3 {
  margin: 2rem 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.sobre-card p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.sobre-card ul {
  margin: 0;
  padding-left: 1.5rem;
  color: var(--text-secondary);
  line-height: 1.8;
}

.sobre-card li {
  margin-bottom: 0.5rem;
}

.sobre-card strong {
  color: var(--text-primary);
  font-weight: 600;
}
</style>

