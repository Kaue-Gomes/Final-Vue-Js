<template>
  <div class="produto-card">
    <div class="produto-imagem">
      <img :src="imagemUrl" :alt="produto.nome" />
      <div class="produto-badges">
        <span v-if="produto.estoque < 10" class="badge badge-warning">Estoque Baixo</span>
        <span v-if="!produto.ativo" class="badge badge-danger">Inativo</span>
      </div>
    </div>
    
    <div class="produto-content">
      <div class="produto-header">
        <h3 class="produto-nome">{{ produto.nome }}</h3>
        <div class="produto-categoria">{{ produto.categoria || 'Sem categoria' }}</div>
      </div>
      
      <p v-if="produto.descricao" class="produto-descricao">{{ truncate(produto.descricao, 80) }}</p>
      
      <div class="produto-footer">
        <div class="produto-preco">{{ formatCurrency(produto.preco) }}</div>
        <div class="produto-estoque">Estoque: {{ produto.estoque }}</div>
      </div>
      
      <div class="produto-actions">
        <button class="btn btn-icon" @click="$emit('visualizar', produto.id)" title="Visualizar">
          <i class="bi bi-eye"></i>
        </button>
        <button class="btn btn-icon" @click="$emit('editar', produto.id)" title="Editar">
          <i class="bi bi-pencil"></i>
        </button>
        <button class="btn btn-icon btn-danger" @click="$emit('deletar', produto.id)" title="Deletar">
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatCurrency } from '@/utils/formatters'
import { truncate } from '@/utils/helpers'
import { getImageUrl } from '@/utils/helpers'

const props = defineProps({
  produto: {
    type: Object,
    required: true
  }
})

defineEmits(['visualizar', 'editar', 'deletar'])

const imagemUrl = computed(() => getImageUrl(props.produto.imagem_url))
</script>

<style scoped>
.produto-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.produto-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary);
}

.produto-imagem {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.produto-imagem img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.produto-card:hover .produto-imagem img {
  transform: scale(1.05);
}

.produto-badges {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-warning {
  background: var(--color-warning);
  color: white;
}

.badge-danger {
  background: var(--color-danger);
  color: white;
}

.produto-content {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.produto-header {
  margin-bottom: 0.75rem;
}

.produto-nome {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
}

.produto-categoria {
  font-size: 0.85rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.produto-descricao {
  margin: 0 0 1rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
  flex: 1;
}

.produto-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.produto-preco {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
}

.produto-estoque {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.produto-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-icon {
  width: 36px;
  height: 36px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: var(--bg-tertiary);
  transform: scale(1.05);
}

.btn-icon.btn-danger {
  border-color: var(--color-danger);
  color: var(--color-danger);
}

.btn-icon.btn-danger:hover {
  background: var(--color-danger);
  color: white;
}
</style>

