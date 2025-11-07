<template>
  <div class="atividade-recente">
    <div class="atividade-header">
      <h3>Atividades Recentes</h3>
    </div>
    
    <div class="atividade-list">
      <div
        v-for="atividade in atividades"
        :key="atividade.id || atividade.data"
        class="atividade-item"
      >
        <div class="atividade-icon">
          <i :class="getIcon(atividade.tipo)"></i>
        </div>
        <div class="atividade-content">
          <div class="atividade-texto">
            <strong>{{ atividade.produto }}</strong>
            foi {{ atividade.tipo === 'criado' ? 'criado' : 'atualizado' }}
          </div>
          <div class="atividade-data">{{ formatDate(atividade.data) }}</div>
        </div>
      </div>
      
      <div v-if="atividades.length === 0" class="atividade-empty">
        <p>Nenhuma atividade recente</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '@/utils/formatters'

defineProps({
  atividades: {
    type: Array,
    default: () => []
  }
})

const getIcon = (tipo) => {
  return tipo === 'criado' ? 'bi bi-plus-circle' : 'bi bi-pencil'
}
</script>

<style scoped>
.atividade-recente {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.atividade-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.atividade-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.atividade-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.atividade-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.atividade-item:hover {
  background: var(--bg-secondary);
}

.atividade-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  font-size: 1.1rem;
  flex-shrink: 0;
}

.atividade-content {
  flex: 1;
}

.atividade-texto {
  color: var(--text-primary);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.atividade-texto strong {
  font-weight: 600;
}

.atividade-data {
  color: var(--text-tertiary);
  font-size: 0.8rem;
}

.atividade-empty {
  text-align: center;
  padding: 2rem;
  color: var(--text-tertiary);
}

.atividade-empty p {
  margin: 0;
}
</style>

